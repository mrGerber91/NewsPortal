import os
import django
from django.core.mail import send_mail
from django.conf import settings
from dotenv import load_dotenv


load_dotenv()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')
django.setup()

from news.utils import send_weekly_newsletter

# Вызываем функцию send_weekly_newsletter() для выполнения рассылки прямо сейчас
send_weekly_newsletter()
