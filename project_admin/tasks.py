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
logger = get_task_logger(__name__)


@task(name="download_zip_files")
def download_zip_files(user):
    try:
        project = Project.objects.get(user=user)
        file_names = project.file_set.all().values_list('download_url', 'basename', 'id', named=True)
        zip_subdir = str(uuid.uuid4())
        zip_filename = '%s.zip' % zip_subdir
        byte_stream = BytesIO()
        s3_resource = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        with zipfile.ZipFile(byte_stream, 'w') as zf:
            for filename in file_names:
                file_response = requests.get(filename.download_url)
                if file_response.status_code == 200:
                    new_filename = filename.basename + '-' + str(filename.id)
                    with open(new_filename, 'wb') as f:
                        f.write(file_response.content)
                    zip_path = os.path.join(zip_subdir, new_filename)
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
                                                                   'Key': zip_filename}, ExpiresIn=100)
        send_email(download_success, zipfile_url, project.contact_email, project.name)
    except Exception as e:
        logger.error('Downloading zip file crashed', e)
