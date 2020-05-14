from django.contrib import admin
from . import models

class CompeteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',  'desc', 'pic', 'start_time', 'att_cnt']
    list_editable = ['title', 'desc', 'pic', 'start_time']

admin.site.register(models.Competition, CompeteAdmin)