from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post, Subscriber


def send_weekly_newsletter():
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=one_week_ago)

    if new_posts.exists():
        subject = "Новые статьи и новости за последнюю неделю"
        context = {'new_posts': new_posts}

        # Генерируем HTML-сообщение с использованием шаблона
        html_content = render_to_string('weekly_newsletter.html', context)

        # Получаем список подписчиков
        subscribers = Subscriber.objects.all()

        # Отправляем письмо каждому подписчику
        for subscriber in subscribers:
            user_email = subscriber.user.email  # Получаем email пользователя из связанной модели User

            # Создаем объект EmailMultiAlternatives для отправки HTML-сообщения
            email = EmailMultiAlternatives(subject, html_content, 'dj.news.ango@mail.ru', [user_email])
            email.attach_alternative(html_content, "text/html")
            email.send()


