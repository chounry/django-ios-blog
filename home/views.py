
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from .form import post_form
from comment.comment_form import Comment_form

from .models import Post
from comment.models import Comment
from tag.models import Tag

from blog.customFuntion import *

import datetime

def search(request):
    all_post = Post.objects.all()
    query = request.GET.get('q')
    if query:
        all_post = all_post.filter(
            Q(post_title__icontains= query) |
            Q(caption__icontains= query)  |
            Q(tag__icontains= query)
        )
    posts = pageManager(request, all_post, 10)
    context = {'posts':posts}
    return render(request, 'home/blog.html', context)


def home(request):
    print('yes')
    all_post = Post.objects.all()
    allow = False

    trending_tag = Tag.objects.filter(tag_name_length__lt=10)
    random.shuffle(list(trending_tag))
    trending_tag = trending_tag[:11]

    if request.user.is_superuser or request.user.is_staff:
        allow = True
    posts = pageManager(request, all_post, 12)

    right_side_posts = get_query_for_righSide('Apps', 'Jailbreak')

    context = {'posts': posts,
               'allow': allow,
               'trending_tags':trending_tag,
               'latest_posts':get_latest_post(Post),
               'right_side_posts':right_side_posts
               }

    return render(request, 'home/home.html', context )

def dateLookUp(request, year, month = None, day = None):
    date = None

    if month == None and day == None:
        posts = Post.objects.filter(publish_date__year = year)
        if posts:
            date = posts.first().publish_date.strftime("%Y")
    elif day == None:
        posts = Post.objects.filter(publish_date__year = year, publish_date__month = month)
        if posts:
            date = posts.first().publish_date.strftime("%d %B")
    else:
        posts = Post.objects.filter(publish_date__year = year, publish_date__month = month, publish_date__day = day)
        if posts:
            date = posts.first().publish_date.strftime("%d %B %Y")

    if posts:
        return render(request, 'tag/tag-filter.html',{'posts':posts, 'date':date})
    else:
        return render(request, 'Additional/NoPageFound.html')

def personal(request):
    return render(request, 'home/personal.html')


def contact(request):
    return render(request, 'home/contact.html')


def CreatePost(request):
    user = request.user.username
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = post_form(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        all_tag = instance.tag.split(',')
        instance.user = request.user
        instance.save()

        all_tag = list(map(noStrip, all_tag))
        for tag in all_tag:
            try:
                exist_tag = Tag.objects.get(tag_name=tag)
            except:
                exist_tag = None

            if exist_tag != None:
                posts_id = convertToInt(exist_tag.post)
                posts_id.append(instance.id)
                exist_tag.post = posts_id
                exist_tag.save()

            else:
                Tag.objects.create(tag_name=tag, post=[instance.id])

        return HttpResponseRedirect(instance.get_absolute_url())

    template_name = 'home/post_form.html'
    context = {'form': form, 'user': user}
    return render(request, template_name, context)


def BlogDetail(request, year, month, day, slug):
    template_name = 'home/blog-detail.html'
    instance = get_object_or_404(Post, slug=slug, publish_date = datetime.date(int(year), int(month), int(day)))
    random_post = Post.objects.exclude(post_title = instance.post_title)
    share_string = [ quote_plus(instance.caption), quote_plus(instance.post_title) ]
    tags = instance.get_tag() # get the tags by its instance

    # <----right side and under the post detail
    try:
        random_posts = random.sample(list(random_post), 3)
    except:
        random_posts = random_post
    right_side_posts = get_query_for_righSide('Apps', 'Jailbreak')
    # right side and under the post detail ----->

    # <----- Comment form
    initial_data = {
        'content_type': instance.get_content_type,
        'obj_id': instance.id
    }

    comment_form = Comment_form(request.POST or None, initial=initial_data)
    if comment_form.is_valid():
        c_type = comment_form.cleaned_data.get('content_type')
        content_type = ContentType.objects.get(model=c_type)
        obj_id = comment_form.cleaned_data.get('obj_id')
        content = comment_form.cleaned_data.get('comment')
        parent_obj = None

        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None

        if parent_id:
            parent_obj = Comment.objects.get(id=parent_id)

        created_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content=content,
            content_type=content_type,
            object_id=obj_id,
            parent=parent_obj,

        )
        return HttpResponseRedirect(created_comment.content_object.get_absolute_url())
    # comment form ----->

    comments = Comment.objects.filter_by_instance(instance)

    # <----- delete | edit comment
    if request.method == 'POST':
        try:
            comment_del = int(request.POST.get('comment_id'))

        except:
            comment_del = None

        if comment_del != None:
            comment_obj = Comment.objects.get(id=comment_del)
            if request.user == comment_obj.user:
                comment_obj.delete()

            return HttpResponseRedirect(instance.get_absolute_url())
    # delete | edit comment ----->

    context = {
        'instance': instance,
        'tags': tags,
        'share_string_caption': share_string[0],
        'share_string_title': share_string[1],
        'comments': comments,
        'comment_form': comment_form,
        'random_posts': random_posts,
        'right_side_posts': right_side_posts

    }
    return render(request, template_name, context)


def delBlog(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    try:
        instance = Post.objects.get(slug = slug)
    except:
        return render(request, 'home/templates/Addit/NoPageFound.html')

    instance.delete()

    return HttpResponseRedirect('/blog/')


def BlogUpdate(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    form = post_form(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    template_name = 'home/post_form.html'
    context = {'form': form}
    return render(request, template_name, context)



# <--- Custom function
def pageManager(request, all_post, amount):
    paginator = Paginator(all_post, amount)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return posts
# End custom function ----->