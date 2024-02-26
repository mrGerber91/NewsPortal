from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .utils import send_weekly_newsletter
from .models import Visitor
from django.db.models.signals import post_save

@receiver(post_migrate, sender=AppConfig)
def send_newsletter_on_startup(sender, **kwargs):
    send_weekly_newsletter()


@receiver(post_save, sender=None)
def increment_visitor_count(sender, instance, created, **kwargs):
    if created:
        visitor = Visitor.objects.first()
        if visitor:
            visitor.count += 1
            visitor.save()
        else:
            Visitor.objects.create(count=1)