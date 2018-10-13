# -*- coding:utf-8 -*-

import logging
import json
import time
import os

from django.http import *
from django.template import loader
from ShadowInk import settings

logger = logging.getLogger(__name__)

# '/<slug>'目录，分别处理，对于未知的slug返回none
# 需要登录才能显示，否则跳转到登录页面
# @login_required
def showPages(request, path):
    logging.info('Accessing Page /%s with showPages'%(path))

    if path=='transform':
        template = loader.get_template('transformDemo.html')
        return HttpResponse(template.render({},request))

    if path=='post':
        pic = request.FILES.get("pic")
        if pic==None:
            result = {
                'message': '没有图片！',
                'src': ''
            }
        else:
            random_name = str(int(time.time())%345678910)#JQKA
            filename = "DEMO_IN_" + random_name + os.path.splitext(pic.name)[1]
            filename2 = "DEMO_OUT_" + random_name + os.path.splitext(pic.name)[1]
            url = os.path.join(settings.MEDIA_URL, filename2)
            urlSave = os.path.join(settings.MEDIA_ROOT, filename)
            urlSave2 = os.path.join(settings.MEDIA_ROOT, filename2)
            with open(urlSave,"wb") as fPic:
                for chunk in pic.chunks():
                    fPic.write(chunk)
            os.system("demo.bat "+urlSave+" "+urlSave2)
            a = 0
            while not os.path.exists(urlSave2) and a<200:
                time.sleep(0.1)
                a+=1
            if a==200:
                # 超时
                result = {
                    'message': '转换超时，请重试！',
                    'src': ''
                }
            else:
                result = {
                    'message' : '转换成功！',
                    'src' : url
                }
        return HttpResponse(json.dumps(result))
    return HttpResponse('No Page Here.')