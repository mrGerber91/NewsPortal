from django.urls import path
from .views import news_list, post_detail, search_news
from .views import NewsCreateView, NewsUpdateView, NewsDeleteView
from .views import ArticleCreateView, ArticleUpdateView, ArticleDeleteView

urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('search/', search_news, name='search_news'),
    path('news/post/<int:post_id>/', post_detail, name='post_detail'),

    # Страницы для новостей
    path('news/create/', NewsCreateView.as_view(), name='create_news'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='edit_news'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='delete_news'),

    # Страницы для статей
    path('articles/create/', ArticleCreateView.as_view(), name='create_article'),
    path('articles/<int:pk>/edit/', ArticleUpdateView.as_view(), name='edit_article'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete_article'),


]

