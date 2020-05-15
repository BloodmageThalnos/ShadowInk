from django.db import models
from django.contrib.auth.models import User

# 图库
class Competition(models.Model):
    class Meta:
        verbose_name = '比赛信息'
        verbose_name_plural = '比赛信息'
    create_date = models.DateTimeField(auto_now_add=True)
    pic = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    desc = models.TextField()
    att_cnt = models.IntegerField(default=0)
    start_time = models.CharField(max_length=50)

class CompAtt(models.Model):
    class Meta:
        verbose_name = '参赛人员管理'
        verbose_name_plural = '参赛人员管理'
    comp = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='compatt_comp_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compatt_user_set')

class CompPic(models.Model):
    class Meta:
        verbose_name = '比赛作品管理'
        verbose_name_plural = '比赛作品管理'
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comppic_user_set')
    comp = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='comppic_comp_set')
    pic = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    create_time = models.CharField(max_length=100, default="2020年5月12日")
    upload_time = models.CharField(max_length=100, default="2020年5月13日")
    desc = models.TextField()