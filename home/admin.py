from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display =('user', 'updated', 'image_tag')
    raw_id_fields =('user',)
    search_fields =('slug', 'caption')
    prepopulated_fields = {'slug': ('caption',)}
    list_filter = ('updated',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_reply', 'created')   
    raw_id_fields = ('user', 'post', 'reply')


admin.site.register(Like)