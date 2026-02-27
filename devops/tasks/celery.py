import os
import celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "config.settings.local"))   

app = celery.Celery('devops')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

