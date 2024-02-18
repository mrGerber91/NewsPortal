from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Author
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .filters import NewsFilter
from django import forms
from .forms import PostForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .mixins import AuthCheckMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.views import View
from django.core.mail import send_mail
from .models import Category
from django.contrib.auth.decorators import login_required
from django.conf import settings


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
    return render(request, 'news/post_detail.html', {'post': post, 'category': category})


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
        form.instance.post_type = 'news'
        user = self.request.user
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
        form.instance.post_type = 'article'
        user = self.request.user
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
                  {'category': category, 'posts': posts, 'subscriber_count': subscriber_count})


@login_required
def subscribe_to_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    category.subscribers.add(request.user)
    return redirect('category_news', category_id=category_id)
