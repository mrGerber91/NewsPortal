from datetime import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Author, Category, Subscriber, UserDailyRecord
from .filters import NewsFilter
from .forms import PostForm
from .exceptions import DailyPostLimitExceeded
from .mixins import AuthCheckMixin

def daily_post_limit_exceeded(request, exception=None):
    return render(request, 'errors/403_2.html', status=403)


@login_required
def increment_post_count(request):
    user = request.user
    today = timezone.now().date()
    record, created = UserDailyRecord.objects.get_or_create(
        user=user, date=today)
    if record.post_count >= 3:
        raise DailyPostLimitExceeded(
            "Вы уже создали максимальное количество записей за сегодня.")
    record.post_count += 1
    record.save()


def news_list(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 10)  # 10 новостей на странице

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'news/news_list.html', {'posts': posts})


def post_detail(request, post_id):
    # Получаем объект поста или возвращаем ошибку 404, если пост не найден
    post = get_object_or_404(Post, pk=post_id)
    post = Post.objects.get(pk=post_id)
    category = post.categories.first()
    return render(request, 'news/post_detail.html',
                  {'post': post, 'category': category})


def search_news(request):
    query = request.GET.get('query', '')

    # Фильтр для поиска по дате
    class DateInput(forms.DateInput):
        input_type = 'date'

    news_filter = NewsFilter(request.GET, queryset=Post.objects.all())

    if 'created_at__gte' in news_filter.form.fields:
        news_filter.form.fields['created_at__gte'].widget = DateInput()

    posts = news_filter.qs.order_by('-created_at')

    paginator = Paginator(posts, 10)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'news/search_results.html',
                  {'posts': posts, 'query': query, 'news_filter': news_filter})


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        # Проверяем, сколько постов пользователь уже создал сегодня
        user = self.request.user
        today = timezone.now().date()
        post_count = UserDailyRecord.objects.filter(
            user=user, date=today).values_list(
            'post_count', flat=True).first()
        if post_count is not None and post_count >= 3:
            return redirect('daily_post_limit_exceeded')

        form.instance.post_type = 'news'
        author = Author.get_author(user)
        form.instance.author = author
        post = form.save()
        category = form.cleaned_data.get('category')
        if category:
            post.categories.add(category)
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                message_text = f'<h1>{post.title}</h1><p>{post.content[:50]}</p>'
                html_message = (f'<p>Здравствуй, {subscriber.username}. '
                                f'Новая статья в твоём любимом разделе!</p>{message_text}')
                send_mail(
                    post.title,
                    '',
                    settings.EMAIL_HOST_USER,
                    [subscriber.email],
                    html_message=html_message
                )
        increment_post_count(self.request)
        return super().form_valid(form)


class NewsUpdateView(AuthCheckMixin, UpdateView):
    model = Post
    template_name = 'news/news_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')


class NewsDeleteView(AuthCheckMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        # Проверяем, сколько постов пользователь уже создал сегодня
        user = self.request.user
        today = timezone.now().date()
        post_count = UserDailyRecord.objects.filter(
            user=user, date=today).values_list(
            'post_count', flat=True).first()
        if post_count is not None and post_count >= 3:
            return redirect('daily_post_limit_exceeded')

        form.instance.post_type = 'article'
        author = Author.get_author(user)
        form.instance.author = author
        post = form.save()
        category = form.cleaned_data.get('category')
        if category:
            post.categories.add(category)
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                message_text = f'<h1>{post.title}</h1><p>{post.content[:50]}</p>'
                html_message = (f'<p>Здравствуй, {subscriber.username}. '
                                f'Новая статья в твоём любимом разделе!</p>{message_text}')
                send_mail(
                    post.title,
                    '',
                    settings.EMAIL_HOST_USER,
                    [subscriber.email],
                    html_message=html_message
                )
        increment_post_count(self.request)
        return super().form_valid(form)


class ArticleUpdateView(AuthCheckMixin, UpdateView):
    model = Post
    template_name = 'news/article_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')


class ArticleDeleteView(AuthCheckMixin, DeleteView):
    model = Post
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('news_list')


class MyView(PermissionRequiredMixin, View):
    permission_required = 'news.add_post'


class AddPost(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    permission_required = 'news.add_post'


def custom_permission_denied(request, exception):
    return render(request, 'errors/403.html', status=403)


def category_news(request, category_id):
    category = Category.objects.get(pk=category_id)
    subscriber_count = category.subscribers.count()
    posts = Post.objects.filter(categories=category)
    is_subscribed = category.subscribers.filter(pk=request.user.pk).exists()
    return render(request, 'news/category_news.html',
                  {'category': category,
                   'posts': posts,
                   'subscriber_count': subscriber_count,
                   'is_subscribed': is_subscribed})


@login_required
def subscribe_to_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    existing_subscriber = Subscriber.objects.filter(
        user=request.user, category=category).exists()
    if not existing_subscriber:
        Subscriber.objects.create(user=request.user, category=category)
    return redirect('category_news', category_id=category_id)


def get_new_articles_for_week():
    end_date = timezone.now().date()
    start_date = end_date - timezone.timedelta(days=7)

    new_articles = Post.objects.filter(created_at__range=[start_date, end_date])

    return new_articles

def send_weekly_newsletter():
    new_articles = get_new_articles_for_week()

    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        # Формирование контекста для шаблона письма
        context = {'subscriber': subscriber, 'new_articles': new_articles}
        # Загрузка HTML-шаблона письма
        html_message = render_to_string('news/weekly_newsletter.html', context)
        # Отправка письма
        send_mail(
            'Еженедельные новости',
            '',
            settings.EMAIL_HOST_USER,
            [subscriber.email],
            html_message=html_message
        )