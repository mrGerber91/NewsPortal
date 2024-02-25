from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .utils import send_weekly_newsletter

@receiver(post_migrate, sender=AppConfig)
def send_newsletter_on_startup(sender, **kwargs):
    send_weekly_newsletter()
