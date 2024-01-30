from django.urls import path
from .views import news_list, post_detail

# Определение маршрутов URL для приложения "news"

urlpatterns = [
    # URL-путь для отображения списка новостей
    path('news/', news_list, name='news_list'),
    # URL-путь для отображения деталей конкретного поста
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]

