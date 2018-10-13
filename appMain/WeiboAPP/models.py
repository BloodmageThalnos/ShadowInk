from django.db import models
from django.contrib.auth.models import User

class Mblog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

class MblogFile(models.Model):
    blog = models.ForeignKey(Mblog, on_delete=models.CASCADE, related_name='files_set')
    file = models.FilePathField()
    is_image = models.BooleanField()
