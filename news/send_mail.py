import os
import django
from django.core.mail import send_mail
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')
django.setup()



def send_test_email():
    subject = 'Тестовое сообщение'
    message = 'Это тестовое сообщение для проверки отправки электронной почты.'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['lalkakapalka3@gmail.com']

    send_mail(subject, message, from_email, to_email)

if __name__ == "__main__":
    send_test_email()
