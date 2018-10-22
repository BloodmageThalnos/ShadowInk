from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set') #关注我的用户
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set') #我关注的用户
    build_date = models.DateTimeField(auto_now_add=True)
    followers_account = models.IntegerField(0,1000)

class PersonalDetials(models.Model): #个人资料
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FilePathField()
    phone = models.CharField(20)
    follow = models.ManyToManyField('self',through='Follow',through_fields=('followers','following'),symmetrical=False)
