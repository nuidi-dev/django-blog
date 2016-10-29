  #-*- encoding: utf-8 -*-
from __future__ import unicode_literals

import re
from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify

class UploadedImage(models.Model):
    source = models.ImageField(upload_to='images/%Y/%m/%d/')

    def __str__(self):
        return self.source.url

class Post(models.Model):
    image = models.ImageField(upload_to='post_img/%Y/%m/%d/', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            c=0
            slug = slugify(self.title)
            while True:
                try:
                    if (c==0): Post.objects.get(slug=slug)
                    else: Post.objects.get(slug="{}-{}".format(slug,c))
                    c+=1
                except Post.DoesNotExist:
                    if (c==0): self.slug = slug
                    else: self.slug = "{}-{}".format(slug, c)
                    break

        super(Post, self).save(*args, **kwargs)

    def split_tags(self):
        return self.tags.split(" ")

    def get_intro(self):
        intro = self.body
        m = re.search(r'(\[h\](.+)?\[/h\])?[\r\n]*(.+)\r', intro)
        if m:
            intro = m.group(3)
        return intro

    def bb_body(self):
        parse_body = self.body

        # HEAD [h]
        regex = r'\[h\](.+?)\[/h\]'
        repl = r'<h4>\1</h4>'
        parse_body = re.sub(regex,repl,parse_body)

        # BOLD [b]
        regex = r'\[b\](.+?)\[/b\]'
        repl = r'<b>\1</b>'
        parse_body = re.sub(regex,repl,parse_body)

        # ITALIC [i]
        regex = r'\[i\](.+?)\[/i\]'
        repl = r'<i>\1</i>'
        parse_body = re.sub(regex,repl,parse_body)

        # LINK [link="http://example.com"]Click![/link]
        regex = r'\[link="(.+?)"\](.+?)\[/link\]'
        repl = r'<a href="\1">\2</a>'
        parse_body = re.sub(regex,repl,parse_body)

        # IMAGE [img]image_source[/img]
        regex = r'\[img\](.+)?\[/img\]'
        repl = r'<img src="\1" />'
        parse_body = re.sub(regex,repl,parse_body)

        # CODE [img]image_source[/img]
        regex = r'\[code\](.*?)\[/code\]'
        repl = r'<pre>\1</pre>'
        parse_body = re.sub(regex,repl,parse_body)

        return mark_safe(parse_body)

class Comment(models.Model):
    post = models.ForeignKey(Post, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user = models.CharField(max_length=15, verbose_name="Your nickname")
    text = models.TextField(verbose_name="Your comment")

    class Meta:
        ordering = ['-created']
