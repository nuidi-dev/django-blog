from django.conf.urls import url, include, handler404
from django.contrib import admin
from .views import BlogIndex, BlogPost, BlogTag

handler404 = 'core.views.nuidi_error_page'

urlpatterns = [
    url(r'^$', BlogIndex, name='blog_index'),
    url(r'^tag/(?P<tag_name>[\w\d-]+)/$', BlogTag, name='blog_tag'),
    url(r'^post/(?P<post_slug>[\w\d-]+)/$', BlogPost, name='blog_post'),
]
