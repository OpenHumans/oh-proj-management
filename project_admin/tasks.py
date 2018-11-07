from io import BytesIO
import zipfile
import requests
import os
import boto3
import uuid
import datetime
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings
from .models import Project, S3Upload
from .utility import send_email
from .helpers import get_all_members, filter_members_group_id, update_members
logger = get_task_logger(__name__)


@task(name='update_project_members')
def update_project_members(project_id):
    project = Project.objects.get(pk=project_id)
    members = get_all_members(project.token)
    update_members(members, project)
    project.refreshed_at = datetime.datetime.now()
    project.save()


@task(name="compile_metadata")
def compile_metadata(user):
    print('start')
    project = Project.objects.get(user=user)
    filename = project.name + "." + str(uuid.uuid4()) + '.project_members.csv'
    print(filename)
    s3_resource = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    members = get_all_members(project.token)
    metadata = "project_member_id\tdate_joined\tnumber_of_files_shared\n"
    for member in members:
        if 'username' in member.keys():
            metadata += "{0}\t{1}\t{2}\t{3}\n".format(
                member['project_member_id'],
                member['username'],
                member['created'],
                len(member['data']))
        else:
            metadata += "{0}\t{1}\t{2}\t{3}\n".format(
                member['project_member_id'],
                '-',
                member['created'],
                len(member['data']))
    s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=filename,
                                                                    Body=metadata,
                                                                    ContentType='text/csv')
    zipfile_url = s3_client.generate_presigned_url('get_object',
                                                   Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                           'Key': filename}, ExpiresIn=86400)
    s3uploaded_file = S3Upload(key=filename)
    s3uploaded_file.save()
    send_email(True, zipfile_url, project.contact_email, project.name)


@task(name="download_zip_files")
def download_zip_files(user, group_id=None):
    try:
        project = Project.objects.get(user=user)
        zip_subdir = str(uuid.uuid4())
        zip_filename = '%s.zip' % zip_subdir
        byte_stream = BytesIO()
        s3_resource = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        if group_id:
            members = filter_members_group_id(project.token, group_id)
        else:
            members = get_all_members(project.token)
        with zipfile.ZipFile(byte_stream, 'w') as zf:
            for member in members:
                for oh_file in member['data']:
                    file_response = requests.get(oh_file['download_url'])
                    if file_response.status_code == 200:
                        new_filename = "{}-{}".format(
                                            oh_file['id'],
                                            oh_file['basename'])
                        with open(new_filename, 'wb') as f:
                            f.write(file_response.content)
                        zip_path = os.path.join(
                                        zip_subdir,
                                        member['project_member_id'],
                                        new_filename)
                        zf.write(new_filename, zip_path)
                        os.unlink(new_filename)
                        download_success = True
                    else:
                        logger.error('File response error- could not be downloaded', file_response)
                        download_success = False
                        zipfile_url = None
                        break
        if download_success:
            zip_contents = byte_stream.getvalue()
            s3_resource.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(Key=zip_filename,
                                                                            Body=zip_contents,
                                                                            ContentType='application/zip')
            zipfile_url = s3_client.generate_presigned_url('get_object',
                                                           Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                   'Key': zip_filename}, ExpiresIn=86400)
            s3uploaded_file = S3Upload(key=zip_filename)
            s3uploaded_file.save()
        send_email(download_success, zipfile_url, project.contact_email, project.name)
    except Exception as e:
        logger.error('Downloading zip file crashed', e)
