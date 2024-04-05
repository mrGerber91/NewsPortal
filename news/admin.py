from django.contrib import admin
from .models import Category, Author, Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'preview_content', 'title', 'created_at')
    search_fields = ('author', 'preview_content', 'title', 'created_at')
    list_filter = ('author', 'created_at')

    def preview_content(self, obj):
        return obj.content[:20] if len(obj.content) > 20 else obj.content

    preview_content.short_description = 'content'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user', 'rating')
    list_filter = ('user', 'rating')

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'subscribers')
    list_filter = ('name', 'subscribers')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'preview_post_title', 'preview_text_title', 'created_at')
    search_fields = ('user', 'post', 'created_at')
    list_filter = ('user', 'post', 'created_at')

    def preview_post_title(self, obj):
        return obj.post.title[:15] if len(obj.post.title) > 15 else obj.post.title

    preview_post_title.short_description = 'Post Title'

    def preview_text_title(self, obj):
        return obj.text[:15] if len(obj.text) > 15 else obj.text

    preview_text_title.short_description = 'Text Title'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
