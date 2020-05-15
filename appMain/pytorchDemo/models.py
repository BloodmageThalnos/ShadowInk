from django.db import models
from django.contrib.auth.models import User

# 图库
class MyPic(models.Model):
    class Meta:
        verbose_name = '用户图册'
        verbose_name_plural = '用户图册'
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pic_user_set')
    create_date = models.DateTimeField(auto_now_add=True)
    picBefore = models.CharField(max_length=100)
    picAfter = models.CharField(max_length=100)
    saved = models.BooleanField(default=False)

class MainPic(models.Model):
    class Meta:
        verbose_name = '首页图片管理'
        verbose_name_plural = '首页图片管理'
    pic = models.CharField(max_length=100)