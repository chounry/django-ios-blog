import re
import random


def convertToInt(String_list):
    int_list = re.findall(r'\d+', String_list)
    return list(map(toInt, int_list))


def toInt(x):
    return int(x)

def noStrip(x):
    return x.strip()


def get_one_post(list_of_instance, instance, pre_post):
    for i in list_of_instance:
        if ((i != instance) and (i not in pre_post)):
            return i


def get_latest_post(query):
    all_posts = query.objects.all()
    try:
        latest_posts = all_posts[:4]
    except:
        latest_posts = all_posts[:]
    return latest_posts


def get_query_for_righSide(middle, bottom):
    from home.models import Post
    from tag.models import Tag

    if not Tag.objects.first() or Tag.objects.count() < 2:
        return

    posts_manage = Post.objects
    all_posts = posts_manage.all()
    tag_manage = Tag.objects
    #<----- Latest post
    try:
        latest_posts = all_posts[:5]
    except:
        latest_posts = all_posts
    # End Latest post ----->

    middle_posts = sorted(posts_manage.filter(tag__contains = middle).exclude(post_title__in = list(latest_posts)[:2]), key= lambda x:random.random())
    bottom_posts = sorted(posts_manage.filter(tag__contains = bottom).exclude(post_title__in = list(latest_posts)[:2] + list(middle_posts)[:2]), key= lambda x:random.random())

    if not middle_posts:
        middle = tag_manage.all().exclude(tag_name=bottom).first().tag_name
        middle_posts = sorted(posts_manage.filter(tag__contains = middle).exclude(post_title__in = list(latest_posts)[:2] + list(bottom_posts)[:2]), key= lambda x:random.random())
    if not bottom_posts:
        bottom = tag_manage.all().exclude(tag_name = middle).last().tag_name
        bottom_posts = sorted(posts_manage.filter(tag__contains = bottom).exclude(post_title__in = list(latest_posts)[:2] + list(middle_posts)[:2]), key= lambda x:random.random())

    middle_posts = middle_posts[:5]
    bottom_posts = bottom_posts[:5]

    total = [ ('Latest', (latest_posts)), (middle, (middle_posts)), (bottom, (bottom_posts)) ]
    return total










