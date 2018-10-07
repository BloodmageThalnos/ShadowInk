from django.contrib import admin
from . import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'pic_url', 'create_date']
    list_editable = ['title', 'author', 'pic_url']

admin.site.register(models.Article, ArticleAdmin)