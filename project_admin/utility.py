from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def send_email(download_success, zipfile_url, contact_email, contact_name):
    if download_success:
        message = 'Hi ' + contact_name + '! Here is the file download link: ' + zipfile_url
    else:
        message = 'File Download Failed. Please try again'
    subject = 'OH-Proj-Management: File Download Requested'
    if subject and message and contact_email:
        try:
            response = send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [contact_email], fail_silently=False)
            if not response:
                logger.error('Email could not be sent')
        except BadHeaderError:
            logger.error('Invalid header found.')
    else:
        logger.error('Make sure all fields are entered and valid.')
