import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from ShadowInk import settings

import random
import os
from django.contrib.auth.models import User
from WeiboAPP.models import *
from WeiboAPP.views import *
from .models import *

logger = logging.getLogger(__name__)

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with main.showPages'%(path))

    if path=='index':
        weibos = getWeiboShown(request.user)
        # userinfo = getUserinfo(request.user)
        template = loader.get_template('PC_mainPage.html')
        context = {
            'weibos' : weibos,
            # 'userinfo' : userinfo,
        }
        return HttpResponse(template.render(context, request))
    if path=='transfer':
        template = loader.get_template('PC_tranPage.html')
        context = {}
        return HttpResponse(template.render(context, request))
    if path=='compete':
        template = loader.get_template('PC_competePage.html')
        context = {}
        return HttpResponse(template.render(context, request))
    if path=='my':
        weibos = getWeiboShown(request.user)
        template = loader.get_template('PC_myPage.html')
        userinfo = getUserinfo(request.user)
        context = {
            'weibos' : weibos,
            'userinfo': userinfo,
        }
        return HttpResponse(template.render(context, request))

    return HttpResponse('No Page Here.')

# '/'目录，显示主页
def showMainPage(request):
    logging.info('Accessing Page / with showMainPage')
    return HttpResponseRedirect('/s/index')


# '/<path>'目录，一般是请求资源或者静态网页，直接分类别发送
def showPath(request, path):
    # logging.info('Accessing Page /%s with showPath'%(path))

    if path.endswith('jpg') or path.endswith('jpeg'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpeg")

    if path.endswith('png'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/png")

    if path.endswith('gif'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/gif")

    if path.endswith('ico'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/x-icon")

    if path.endswith('woff'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="application/x-font-woff")

    if path.endswith('css'):
        with open('./static/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html, content_type="text/css")

    if path.endswith('js'):
        with open('./static/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html, content_type="application/x-javascript")

    if path.endswith('svg'):
        with open('./static/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html, content_type="image/svg+xml")

    if path.endswith('html'):
        with open('./static/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html)

# '/media/...'目录，请求静态资源等。日后部署nginx时可以转移控制权
def showMedia(request, path):
    # logging.info('Accessing Page /%s with showMedia'%(path))

    if path.endswith('jpg') or path.endswith('jpeg'):
        with open('./media/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpeg")

    if path.endswith('png'):
        with open('./media/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/png")

    if path.endswith('gif'):
        with open('./static/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/gif")
