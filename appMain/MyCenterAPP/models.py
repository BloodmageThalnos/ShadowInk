from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):  #用户关注与被关注的记录
    id = models.AutoField(primary_key = True)
    follower = models.ForeignKey('PersonalDetails', on_delete=models.CASCADE, related_name='followers_set')
    following = models.ForeignKey('PersonalDetails', on_delete=models.CASCADE, related_name='following_set')
    build_date = models.DateTimeField(auto_now_add=True)

class PersonalDetails(models.Model): #个人资料
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.FilePathField()
    phone = models.CharField(max_length=11)
    bg_img = models.FilePathField()
    introduction = models.TextField()
    address = models.TextField()
    follow = models.ManyToManyField("self",through=Follow,through_fields=("follower","following"),symmetrical=False)
