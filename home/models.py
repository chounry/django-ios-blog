from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, pre_delete
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from markdown_deux  import markdown
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.fields import GenericRelation

from tag.models import Tag
from comment.models import Comment

from blog.customFuntion import *


class PostManager(models.Manager):
    def get_post_by_tag(self, instance):
        posts_id = convertToInt(instance.post)
        posts_obj = list(map(lambda id:super(PostManager,self).get(id = id), posts_id))
        return posts_obj

# Create your models here.
class Post(models.Model):
    # tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    caption = models.TextField(max_length = 5000)
    post_img = models.FileField(blank = True, null= True)
    post_title = models.CharField(max_length = 100, db_index= True)
    publish_datetime = models.DateTimeField(auto_now_add = False, auto_now=True)
    publish_date = models.DateField(auto_now=True, auto_now_add= False)
    slug = models.SlugField(unique= True, editable=False)
    tag = models.CharField(max_length=2000, validators=[])
    comment = GenericRelation(Comment)

    objects = PostManager()

    def get_absolute_url(self):
        kwargs = {'slug':self.slug,
                  'year':self.publish_date.year,
                  'month':self.publish_date.month,
                  'day':self.publish_date.day
                  }
        return reverse('home:blog-detail',kwargs= kwargs)

    def __str__(self):
        return self.post_title + ' - ' + self.slug

    def get_markdown(self):
        content = self.caption
        marked_content = markdown(content)
        return mark_safe(marked_content)

    class Meta:
        ordering = ['-publish_datetime']

    # @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def get_tag(self):
        instance = self
        original_tag = re.findall(r'(\w+[-\s&\w]*)',instance.tag)  # take the tag in the string of list from db
        tags_wit_minus = list(map(slugify, original_tag ))#  for url
        dict_tag = {}
        for i in range(len(original_tag)):
            wit_minus = tags_wit_minus[i]
            original = original_tag[i]
            dict_tag[original] = wit_minus

        return dict_tag

    def amount_comment(self):
        instance = self
        return instance.comment.count()


def create_slug(instance, new_slug = None):
    slug = slugify(instance.post_title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug = slug)
    exist = qs.exists()
    if exist:
        new_slug = "%s-%s"%(slug, random.randint(0, Post.objects.count()))
        return new_slug
    return slug

def create_tag_post_modal(instance):
    tags = list(map(noStrip, instance.tag.split(',')))
    return tags


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    instance.tag = create_tag_post_modal(instance)

pre_save.connect(pre_save_post_receiver, sender= Post)




def del_idIn_Tag(instance):
    tags = re.findall(r'(\w+[-\s&\w]*)', instance.tag)
    for tag in tags:
        try:
            tag_obj = Tag.objects.get(tag_name = tag)
        except:
            tag_obj = None

        if tag_obj:
            posts_id = convertToInt(tag_obj.post)
            if len(posts_id) == 1:  # if there is only one id in the Tag.post Model then delete itself
                tag_obj.delete()

            elif instance.id in posts_id:
                posts_id.remove(instance.id)
                tag_obj.post = posts_id
                tag_obj.save()


def pre_delete_post_receiver(sender, instance, *args, **kwargs):
    del_idIn_Tag(instance)

pre_delete.connect(pre_delete_post_receiver, sender= Post)











