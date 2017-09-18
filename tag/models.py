from django.db import models
from django.db.models.signals import  pre_save
from django.utils.text import slugify

from blog.customFuntion import *
#import blog.customFuncFtModel as FuncFtModel

class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    url_tag_name = models.SlugField(editable= False)
    post = models.CharField(max_length= 1000, validators=[])
    tag_name_length = models.PositiveIntegerField(null = True)

    def __str__(self):
        return str(self.tag_name)

def calculate_length_name(instance):
    return len(instance.tag_name)

def create_url_tag(instance):
    return slugify(instance.tag_name)


def pre_save_tag_receiver(instance, sender, *args, **kwargs):
    instance.url_tag_name = create_url_tag(instance)
    instance.tag_name_length = calculate_length_name(instance)

pre_save.connect(pre_save_tag_receiver, sender=Tag )

