import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')
app = Celery('NewPortal_v2')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_max_loop_interval = 10

app.conf.beat_schedule = {
    'send-weekly-newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',
        'schedule': 20.0,  # каждые 20 секунд
        #'schedule': crontab(minute=0, hour=8, day_of_week=1), # Запуск каждый понедельник в 8:00
    },
}