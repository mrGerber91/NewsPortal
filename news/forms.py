from django import forms
from .models import Post, Author, Category
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'content']
        labels = {
            'title': 'Заголовок',
            'category': 'Категория',
            'content': 'Содержание новости',
            'author': 'Автор',
        }

    author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())
