# -*- coding:utf-8 -*-

import logging
import json
import time
import os

from django.http import *
from django.template import loader
from ShadowInk import settings
from .models import MyPic

logger = logging.getLogger(__name__)

# '/<slug>'目录，分别处理，对于未知的slug返回none
def transfer(request):
    pic = request.FILES.get("pic")
    if not request.user or not request.user.username:
        result = {
            'message': '未登录，请登录后再创作。',
            'src': ''
        }
    elif not pic:
        result = {
            'message': '请上传需要转换的图片。',
            'src': ''
        }
    else:
        random_name = str(int(time.time())%34567890)
        filename = random_name + os.path.splitext(pic.name)[1]
        picIn = os.path.join(settings.TRANSFER_INPUT, filename)
        picOut = os.path.join(settings.TRANSFER_OUTPUT, filename)
        with open(picIn,"wb") as fPic:
            for chunk in pic.chunks():
                fPic.write(chunk)
        a = 0
        while not os.path.exists(picOut) and a<10: # wait 10 s
            time.sleep(0.1)
            a+=0.1
        if a>=10: # 超时
            result = {
                'message': '转换超时，请重试！',
                'src': ''
            }
        else:
            myPic = MyPic(author=request.user, picBefore='/transfer_input/' + filename, picAfter='/transfer_output/' + filename)
            myPic.save()
            result = {
                'message' : '转换成功！',
                'src' : '/transfer_output/' + filename
            }
    return HttpResponse(json.dumps(result))