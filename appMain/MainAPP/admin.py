from django.contrib import admin
from . import models

class CompeteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',  'desc', 'pic', 'start_time', 'att_cnt']
    list_editable = ['title', 'desc', 'pic', 'start_time']

class CompeteAttAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'comp']
    list_editable = []

class CompetePicAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'pic', 'title', 'desc', 'create_time', 'upload_time', 'comp']
    list_editable = ['pic', 'title', 'desc', 'create_time', 'upload_time']

admin.site.register(models.Competition, CompeteAdmin)
admin.site.register(models.CompAtt, CompeteAttAdmin)
admin.site.register(models.CompPic, CompetePicAdmin)

