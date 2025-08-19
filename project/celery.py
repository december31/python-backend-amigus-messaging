import os

from celery import Celery

# Set the default Django settings module so Celery knows about your Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Create Celery app instance with Django project name
app = Celery('project')

# Load Celery config from Django settings, using `CELERY_` namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps (looks for tasks.py in each app)
app.autodiscover_tasks()
