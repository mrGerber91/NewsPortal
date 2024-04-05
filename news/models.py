from django.db import models
from django.contrib.auth.models import User
import django_filters
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache


class UserDailyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    post_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

# Модель для автора


class Author(models.Model):
    # Один к одному с моделью пользователя Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    @staticmethod
    def get_author(user):
        author, created = Author.objects.get_or_create(user=user)
        return author

    def update_rating(self):
        # Обновление рейтинга автора
        post_rating = sum(post.rating for post in self.post_set.all()) * 3
        comment_rating = sum(
            comment.rating for comment in Comment.objects.filter(
                post__author=self))
        post_comment_rating = sum(comment.rating
                                  for post in self.post_set.all()
                                  for comment in Comment.objects.filter(post=post))

        self.rating = post_rating + comment_rating + post_comment_rating
        self.save()


# Модель для категории
class Category(models.Model):
    name = models.CharField(max_length=255)
    subscribers = models.ManyToManyField(User, through='Subscriber')

    def __str__(self):
        return self.name

    def subscribe_to_category(request, category_id):
        # Ваша логика подписки на категорию здесь
        return redirect('category_news', category_id=category_id)


# Модель для поста
class Post(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)  # Ссылка на автора
    post_type_choices = [('article', 'Article'), ('news', 'News')]
    post_type = models.CharField(max_length=10, choices=post_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    # Связь многие ко многим с категориями
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.content[:124]}..."

    @staticmethod
    def get_new_posts_for_newsletter():
        one_week_ago = timezone.now() - timezone.timedelta(days=7)
        return Post.objects.filter(created_at__gte=one_week_ago)

    def get_absolute_url(self):
        base_url = "http://127.0.0.1:8000/"
        return base_url + reverse('post_detail', kwargs={'post_id': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post_{self.pk}')


# Промежуточная модель для связи Post и Category
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Модель для комментария
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Ссылка на пост
    # Ссылка на пользователя Django
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class NewsFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='From (YYYY-MM-DD)')

    class Meta:
        model = Post
        fields = ['title', 'author__user__username']


class MyPermissions(models.Model):
    class Meta:
        managed = False  # Не управляемая модель
        default_permissions = ()  # Отключаем стандартные разрешения
        permissions = (
            ('add_post', 'Can add post'),
            ('change_post', 'Can change post'),
        )


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.category.name}"


class Visitor(models.Model):
    count = models.IntegerField(default=0)

    @receiver(post_save, sender=None)
    def increment_visitor_count(sender, instance, created, **kwargs):
        if created:
            visitor = Visitor.objects.first()
            if visitor:
                visitor.count += 1
                visitor.save()
            else:
                Visitor.objects.create(count=1)
