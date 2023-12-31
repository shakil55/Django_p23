from django.contrib import admin
from .models import *


admin.site.register(BlogPost)
# admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'approved', 'content')