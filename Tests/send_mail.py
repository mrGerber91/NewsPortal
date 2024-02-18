import os
import django
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv


load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')
django.setup()


def send_test_email():
    тема = 'Тестовое сообщение'
    сообщение = 'Это тестовое сообщение для проверки отправки электронной почты.'
    отправитель = settings.EMAIL_HOST_USER
    получатель = os.getenv('HOST_eMAIL')

    send_mail(тема, сообщение, отправитель, [получатель])


if __name__ == "__main__":
    send_test_email()

