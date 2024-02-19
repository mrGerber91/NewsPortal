import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')

django.setup()

from django.contrib.auth.models import User
from news.models import Category, Subscriber

def check_subscription(username, category_id):
    try:
        user = User.objects.get(username=username)

        category = Category.objects.get(pk=category_id)

        is_subscribed = Subscriber.objects.filter(user=user, category=category).exists()

        if is_subscribed:
            print(f"Пользователь {username} подписан на категорию с ID {category_id}.")
        else:
            print(f"Пользователь {username} не подписан на категорию с ID {category_id}.")
    except User.DoesNotExist:
        print(f"Пользователь с именем пользователя {username} не найден.")
    except Category.DoesNotExist:
        print(f"Категория с ID {category_id} не найдена.")

check_subscription('miklegerber', 1)
