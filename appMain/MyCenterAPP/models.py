from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model): #关注我的用户
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    build_date = models.DateTimeField(auto_now_add=True)
    followers_account = models.IntegerField(0,1000)

class Follow(models.Model):   #我关注的用户
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    build_date = models.DateTimeField(auto_now_add=True)
    following_account = models.IntegerField(0, 1000)

class PersonalDetials(models.Model): #个人资料
    user = models.OneToOneField(User)
    avatar = models.FilePathField()
    phone = models.CharField(20)