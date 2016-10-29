#-*- encoding: utf-8 -*-
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm

def BlogIndex(request):
    last_posts = Post.objects.all()[:10]
    return render( request, 'blog/index.html', { 'last_posts': last_posts } )

def BlogPost(request, post_slug):

    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                vis_ip = request.META['HTTP_X_REAL_IP']
            except KeyError:
                vis_ip = "0.0.0.0"
            comment = comment_form.save(commit=False)
            comment.ip = vis_ip
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog_post', args=(post.slug,))+"#comments")
    else:
        comment_form = CommentForm()

    last_posts = Post.objects.all().order_by('-created')[:10]
    comments = Comment.objects.filter(post=post)

    return render( request, 'blog/post.html', { 'comments': comments, 'post': post, 'last_posts': last_posts, 'comment_form': comment_form } )

def BlogTag(request, tag_name):

    posts = Post.objects.filter(tags__icontains=tag_name)

    return render( request, 'blog/tag.html', { 'posts': posts, 'tag': tag_name } )
