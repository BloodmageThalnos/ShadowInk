from django.contrib import admin
from . import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title',  'author', 'content', 'pic_url']
    list_editable = ['title', 'content', 'pic_url']

admin.site.register(models.Article, ArticleAdmin)
admin.site.site_header = '水墨画创作交流 - 后台管理'
admin.site.site_title = '后台管理'
admin.site.index_title = '水墨画创作交流平台'