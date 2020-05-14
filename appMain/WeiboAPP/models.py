from django.db import models
from django.contrib.auth.models import User

class Mblog(models.Model):
    class Meta:
        verbose_name = '用户动态'
        verbose_name_plural = '用户动态'
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_author_set')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    thumb = models.ManyToManyField(User, related_name='blog_thumb_set')
    comment = models.ManyToManyField(User, through='MblogComment', related_name='blog_comment_set')

class MblogComment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, related_name='comment_author_set')
    blog = models.ForeignKey(Mblog, on_delete=models.CASCADE, related_name='comment_blog_set')
    refer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='comment_refer_set')
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    thumb = models.ManyToManyField(User, related_name='comment_thumb_set')
    content = models.TextField()

class MblogFile(models.Model):
    class Meta:
        verbose_name = '用户动态附件'
        verbose_name_plural = '用户动态附件'
    blog = models.ForeignKey(Mblog, on_delete=models.CASCADE, related_name='blog_files_set')
    file = models.CharField(max_length=100)
    is_image = models.BooleanField()
