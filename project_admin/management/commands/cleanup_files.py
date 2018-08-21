from django.core.management.base import BaseCommand
import datetime
from django.conf import settings
from project_admin.models import S3Upload
from datetime import timedelta
import boto3


class Command(BaseCommand):
    help = 'Delete stale zip files'

    def handle(self, *args, **options):
        s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        old_files = S3Upload.objects.filter(
            created_at__date__lt=datetime.datetime.now() - timedelta(hours=24))
        for of in old_files:
            delete_response = s3_client.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=of.key)
            if delete_response.get("ResponseMetadata").get('HTTPStatusCode') != 204:
                print("Couldn't delete file {}".format(of.key))
        old_files.delete()
