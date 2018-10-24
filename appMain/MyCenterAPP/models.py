from django.db import models
from django.contrib.auth.models import User

<<<<<<< HEAD
class Follow(models.Model):  #用户关注与被关注的记录
    id = models.AutoField(primary_key = True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    build_date = models.DateTimeField(auto_now_add=True)




class PersonalDetials(models.Model): #个人资料
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.FilePathField()
    phone = models.CharField(max_length=11)
    bg_img = models.FilePathField()
    introduction = models.TextField()
    address = models.TextField()
    follow = models.ManyToManyField("self",through=Follow,through_fields=("follower","following"),symmetrical=False)
=======
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
>>>>>>> 3220f7581d55e442160d844c5f5075f4ac6bfe7a
