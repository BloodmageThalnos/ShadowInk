from django.contrib import admin
from . import models

class MBlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'create_date', 'content']
    list_editable = ['content']

class MFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog', 'file', 'is_image']
    list_editable = ['file']

admin.site.register(models.MblogFile, MFileAdmin)
admin.site.register(models.Mblog, MBlogAdmin)
