from django.contrib import admin
from . import models

class MyPicAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'create_date', 'picBefore', 'picAfter']
    list_editable = ['picBefore', 'picAfter']

admin.site.register(models.MyPic, MyPicAdmin)
