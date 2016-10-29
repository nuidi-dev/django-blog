from django.contrib import admin
from .models import Post, UploadedImage, Comment

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(UploadedImage)
