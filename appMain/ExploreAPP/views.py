# -*- coding:utf-8 -*-

import logging
import json
import time
import os

from django.contrib.auth.decorators import login_required
from django.http import *
from django.template import loader
from django.contrib.auth import login
from ShadowInk import settings, mysqlConnector
from . import models

logger = logging.getLogger(__name__)

# '/<slug>'目录，分别处理，对于未知的slug返回none
# 需要登录才能显示，否则跳转到登录页面
# @login_required
def showPages(request, path):
    logging.info('Accessing Page /%s with showPages'%(path))

    if path=='explore':
        template = loader.get_template('mainPage.html')
        return HttpResponse(template.render({},request))

    if path=='article':
        template = loader.get_template('postArticle.html')
        return HttpResponse(template.render({},request))

    # 动态显示首页上的内容
    # TODO: 需要对文章进行排序并处理
    if path=='pContent':
        articles = mysqlConnector.getArticles()
        template = loader.get_template('innerPage1.html')
        context = {
            'articles' : articles
        }
        return HttpResponse(template.render(context, request))

    if path=='pPostArticle':
        title = request.POST.get("title")
        content = request.POST.get("content")
        pic = request.FILES.get("picture")
        if request.user == None:
            result = {
                'success' : 'False',
                'message' : '登录状态错误，请保存你输入的内容，然后刷新页面重试。'
            }
            return HttpResponse(json.dumps(result))
        user = request.user
        if not title :
            result = {
                'success' : 'False',
                'message' : '请输入标题！'
            }
            return HttpResponse(json.dumps(result))
        filename = user.username + "_" + str(int(time.time())) + os.path.splitext(pic.name)[1]
        url = os.path.join(settings.MEDIA_URL, filename)
        urlSave = os.path.join(settings.MEDIA_ROOT, filename)
        with open(urlSave,"wb") as fPic:
            for chunk in pic.chunks():
                fPic.write(chunk)
        insertResult = mysqlConnector.insertArticle(user,title,url,content)
        result = {
            'success' : 'True',
            'message' : '发表文章成功！'
        }
        return HttpResponse(json.dumps(result))

    return HttpResponse('No Page Here.')