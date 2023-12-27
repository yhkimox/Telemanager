from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
# 게시글(Post) Model을 불러옵니다

admin.site.register(Comment)