from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from .models import Tag
from home.models import Post

from blog.customFuntion import *

def tagView(request, tag):
    template = 'tag/tag-filter.html'
    try:
        tag_obj = Tag.objects.get(url_tag_name = tag)

    except:
        return render(request, 'Additional/NoPageFound.html')


    right_side_posts = get_query_for_righSide('Apps', 'Jailbreak')

    posts_obj = Post.objects.get_post_by_tag(tag_obj)

    # <----- Paginator
    paginator = Paginator(posts_obj, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # End Paginator ------>

    context ={
        'posts':posts,
        'tag_name':tag_obj.tag_name,
        'latest_posts': get_latest_post(Post),
        'right_side_posts':right_side_posts

    }
    return render(request, template, context)


