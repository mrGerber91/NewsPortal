from django import forms
from .models import Post, Author
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'content']
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание новости',
            'author': 'Автор',
        }
    author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())