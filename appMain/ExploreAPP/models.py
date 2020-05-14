from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Article(models.Model):
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    pic_url = models.CharField(max_length=150)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

