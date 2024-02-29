from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from .tasks import send_weekly_newsletter
        from .scheduler import news_scheduler
        print('started')

        news_scheduler.add_job(
            id='send weekly',
            func=send_weekly_newsletter,
            trigger=CronTrigger(day_of_week='mon', hour=8, minute=0)
        )
        news_scheduler.start()
