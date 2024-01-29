from django.urls import path
from .views import news_list, post_detail

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
]

