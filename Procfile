release: python manage.py migrate
web: gunicorn oh_proj_management.wsgi --log-file -
worker: celery worker -A oh_proj_management --concurrency=1
