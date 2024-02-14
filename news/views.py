from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .filters import NewsFilter
from django import forms
from .forms import PostForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .mixins import AuthCheckMixin



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
    return render(request, 'news/post_detail.html', {'post': post})


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


class NewsCreateView(AuthCheckMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)

class NewsUpdateView(AuthCheckMixin, UpdateView):
    model = Post
    template_name = 'news/news_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)


class NewsDeleteView(AuthCheckMixin, DeleteView):
    model = Post
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'news'
        return super().form_valid(form)



class ArticleCreateView(AuthCheckMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_form.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'article'
        return super().form_valid(form)


class ArticleUpdateView(AuthCheckMixin, UpdateView):
    model = Post
    template_name = 'news/article_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'article'
        return super().form_valid(form)

class ArticleDeleteView(AuthCheckMixin, DeleteView):
    model = Post
    template_name = 'news/article_confirm_delete.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.post_type = 'article'
        return super().form_valid(form)