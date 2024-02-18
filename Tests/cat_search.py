import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewPortal_v2.settings')

django.setup()

from news.models import Post


def check_posts_without_category():
    posts_without_category = Post.objects.filter(categories=None)

    if posts_without_category.exists():
        print("Статьи и новости без категории:")
        for post in posts_without_category:
            print(f"ID: {post.id}, Заголовок: {post.title}")
    else:
        print("Все статьи и новости имеют категорию.")


if __name__ == "__main__":
    check_posts_without_category()
