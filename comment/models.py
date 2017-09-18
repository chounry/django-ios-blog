from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        instance_id = instance.id
        return super(CommentManager, self).filter(content_type = content_type, object_id = instance_id, parent = None)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='comment_set')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = CommentManager()

    class Meta:
        ordering = ['-publish']

    def children(self):
        return Comment.objects.filter(parent = self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        else:
            return True

    def __str__(self):
        return str(self.content) + ' - ' + str(self.content_object)


