# -*- coding:utf-8 -*-

import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from ShadowInk import settings
from .models import Mblog, MblogFile


import random
import os
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def getWeiboShown():
    weibos = [];
    blogs = Mblog.objects.all()
    for blog in blogs:
        weibos.append({'blog':blog,'pics':blog.files_set.all()})
    return weibos

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with weibo.showPages'%(path))

    if path=='index':
        weibos = getWeiboShown()
        template = loader.get_template('weibo.html')
        for weibo in weibos:
            logger.info(weibo)
            logger.info(weibo['blog'])
            logger.info(weibo['pics'])
        context = {
            'weibos' : weibos
        }
        return HttpResponse(template.render(context, request))

    if path=='postWeibo':
        content = request.POST.get("content")
        if not content or len(content)<5:
            result = {
                'success' : 'False',
                'message' : '请输入至少三个字！'
            }
            return HttpResponse(json.dumps(result))
        files = []
        for i in range(1,10):
            try:
                file = request.FILES.get("file"+str(i))
                if file==None: break
                files.append(file)
            except:
                break
        if request.user == None:
            result = {
                'success' : 'False',
                'message' : '登录状态错误，请登录后再发表。'
            }
            return HttpResponse(json.dumps(result))
        user = User.objects.all()[0]
        mblog = Mblog(author=user,content=content)
        mblog.save()
        for file in files:
            filename = user.username + "_" + str(random.randint(0,777777)) + os.path.splitext(file.name)[1]
            url = os.path.join(settings.MEDIA_URL, filename)
            urlSave = os.path.join(settings.MEDIA_ROOT, filename)
            with open(urlSave,"wb") as fPic:
                for chunk in file.chunks():
                    fPic.write(chunk)
            mbfile = MblogFile(blog=mblog, file=url, is_image=True)# TODO: 判断文件是否为图片
            mbfile.save()
        result = {
            'success' : 'True',
            'message' : '发表分享成功！'
        }
        return HttpResponse(json.dumps(result))

    return HttpResponse('No Page Here.')
