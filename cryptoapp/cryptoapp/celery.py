from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cryptoapp.settings')

# Create Celery app
app = Celery('cryptoapp')

# Load Celery config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks from installed apps
app.autodiscover_tasks()