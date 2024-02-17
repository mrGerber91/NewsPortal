from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(user_signed_up)
def send_welcome_email(sender, **kwargs):
    user = kwargs['user']
    subject = 'Добро пожаловать!'
    message = 'Добро пожаловать на наш сайт!'
    send_mail(subject, message, 'dj.news.ango@mail.ru', [user.email])
