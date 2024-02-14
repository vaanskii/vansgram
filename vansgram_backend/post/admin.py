from django.contrib import admin

from .models import Post,PostAttachment, Comment

admin.site.register(PostAttachment)
admin.site.register(Post)
admin.site.register(Comment)