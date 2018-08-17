from io import BytesIO
import zipfile
import requests
import os
import boto3
import uuid
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.conf import settings
from .models import Project
from .utility import send_email
from .helpers import get_all_members
logger = get_task_logger(__name__)


@task(name="download_zip_files")
def download_zip_files(user):
    try:
        project = Project.objects.get(user=user)
        zip_subdir = str(uuid.uuid4())
        zip_filename = '%s.zip' % zip_subdir
        byte_stream = BytesIO()
        s3_resource = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
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
        send_email(download_success, zipfile_url, project.contact_email, project.name)
    except Exception as e:
        logger.error('Downloading zip file crashed', e)
