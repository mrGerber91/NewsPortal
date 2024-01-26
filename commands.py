# Создание пользователей и объектов модели Author:
from django.contrib.auth.models import User
from news.models import Author

user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавление категорий в модель Category:
from news.models import Category

category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')

# Добавление статей и новости с категориями:
from news.models import Post, PostCategory

post1 = Post.objects.create(author=author1, post_type='article', title='Article 1', content='Content 1')
post1.categories.add(category1, category2)

post2 = Post.objects.create(author=author2, post_type='article', title='Article 2', content='Content 2')
post2.categories.add(category3, category4)

news1 = Post.objects.create(author=author1, post_type='news', title='News 1', content='News Content 1')
news1.categories.add(category1)

# Создание комментариев:
from news.models import Comment

comment1 = Comment.objects.create(post=post1, user=user1, text='Comment 1')
comment2 = Comment.objects.create(post=post2, user=user2, text='Comment 2')
comment3 = Comment.objects.create(post=news1, user=user1, text='Comment 3')
comment4 = Comment.objects.create(post=news1, user=user2, text='Comment 4')

# Применение методов like() и dislike():
post1.like()
post2.dislike()
comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновление рейтингов пользователей:
author1 = Author.objects.get(id=1)
author2 = Author.objects.get(id=2)
author1.update_rating()
author2.update_rating()

# Вывод имени и рейтинга лучшего пользователя
best_user = Author.objects.all().order_by('-rating').first()
print(f"Best User: {best_user.user.username}, Rating: {best_user.rating}")

# Вывод информации о лучшей статье
best_post = Post.objects.all().order_by('-rating').first()
print(f"Date: {best_post.created_at}, Author: {best_post.author.user.username}, Rating: {best_post.rating}")
print(f"Title: {best_post.title}")
print(f"Preview: {best_post.preview()}")

# Вывод всех комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f"Date: {comment.created_at}, User: {comment.user.username}, Rating: {comment.rating}")
    print(f"Text: {comment.text}")



