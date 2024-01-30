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
best_user_data = Author.objects.order_by('-rating').values('user__username', 'rating').first()

if best_user_data:
    print(f"Best User: {best_user_data['user__username']}, Rating: {best_user_data['rating']}")
else:
    print("No users available.")

# Вывод информации о лучшей статье
best_post_data = Post.objects.all().order_by('-rating').values('created_at', 'author__user__username', 'rating', 'title').first()

if best_post_data:
    print(f"Date: {best_post_data['created_at']}")
    print(f"Author: {best_post_data['author__user__username']}")
    print(f"Rating: {best_post_data['rating']}")
    print(f"Title: {best_post_data['title']}")
else:
    print("No posts available.")

# Вывод всех комментариев к лучшей статье
comments_for_best_post = Comment.objects.filter(post__title=best_post_data['title'])
if comments_for_best_post.exists():
        print(f"\nComments for the Best Post '{best_post_data['title']}':")
        for comment in comments_for_best_post:
            print(f"Author: {comment.user.username}")
            print(f"Content: {comment.text}")
            print("--------")