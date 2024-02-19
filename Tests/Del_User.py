import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')

django.setup()

from django.contrib.auth.models import User
from news.models import Category, Subscriber
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount


def delete_user(username):
    try:
        user = User.objects.get(username=username)

        # Удаление адресов электронной почты пользователя
        EmailAddress.objects.filter(user=user).delete()

        # Удаление связанных социальных аккаунтов пользователя
        SocialAccount.objects.filter(user=user).delete()

        # Удаление самого пользователя
        user.delete()

        print(f"Пользователь {username} и все его данные успешно удалены.")
    except User.DoesNotExist:
        print(f"Пользователь с именем пользователя {username} не найден.")


# Замените 'username' на имя пользователя, данные которого вы хотите удалить
delete_user('miklegerber')
