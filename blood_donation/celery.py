import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_donation.settings')

app = Celery('blood_donation')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Celery Beat Schedule
app.conf.beat_schedule = {
    'send-donation-reminders': {
        'task': 'notifications.tasks.send_donation_reminders',
        'schedule': 86400.0,  # Every 24 hours
    },
    'cleanup-expired-requests': {
        'task': 'requests.tasks.cleanup_expired_requests',
        'schedule': 3600.0,  # Every hour
    },
    'update-donor-availability': {
        'task': 'donors.tasks.update_donor_availability',
        'schedule': 43200.0,  # Every 12 hours
    },
    'generate-daily-analytics': {
        'task': 'analytics.tasks.generate_daily_analytics',
        'schedule': 86400.0,  # Every 24 hours
    },
}