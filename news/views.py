from django.shortcuts import render, get_object_or_404
from .models import Post


def news_list(request):
    posts = Post.objects.all().order_by('-created_at')  # Сортировка от более свежей к старой
    return render(request, 'news/news_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'news/post_detail.html', {'post': post})
