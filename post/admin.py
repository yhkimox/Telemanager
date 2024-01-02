from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    
    
admin.site.register(Post, PostAdmin)
