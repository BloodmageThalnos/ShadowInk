from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Picture(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pic_author_set')
    create_date = models.DateTimeField(auto_now_add=True)
    pic = models.FilePathField()
    title = models.CharField(max_length=60)
    descri = models.TextField()
    # thumb = models.ManyToManyField(User, related_name='blog_thumb_set')
    # comment = models.ManyToManyField(User, through='MblogComment', related_name='blog_comment_set')
