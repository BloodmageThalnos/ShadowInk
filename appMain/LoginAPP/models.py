from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    mobile_no = models.CharField(max_length=20)
    avatar = models.FilePathField()


