from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title', 'content']

    title = forms.CharField(label='Заголовок')
    content = forms.CharField(label='Содержание новости', widget=forms.Textarea)
    author = forms.ModelChoiceField(label='Автор', queryset=User.objects.exclude(is_superuser=True))