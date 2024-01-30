from django.shortcuts import render, get_object_or_404
from .models import Post


def news_list(request):
    # Получаем все посты, сортированные по дате создания от более свежих к старым
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'posts': posts})

def post_detail(request, post_id):
    # Получаем объект поста или возвращаем ошибку 404, если пост не найден
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/post_detail.html', {'post': post})
