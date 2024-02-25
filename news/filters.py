import django_filters
from .models import Post
from django_filters import DateFilter
from django import forms


class NewsFilter(django_filters.FilterSet):
    date_from = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Создано после (ГГГГ-ММ-ДД)',
        widget=forms.DateInput(
            attrs={
                'type': 'date'}))

    title = django_filters.CharFilter(
        label='Название', lookup_expr='icontains')
    author__user__username = django_filters.CharFilter(
        label='Имя автора', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'date_from']
