import logging
import json
from django.http import *
from django.template import loader
from ShadowInk import settings

import random
import os
import time
from django.contrib.auth.models import User
from django.contrib.auth import *
from WeiboAPP.models import *
from WeiboAPP.views import *
from pytorchDemo.views import transfer
from .models import *

logger = logging.getLogger(__name__)

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with main.showPages'%(path))

    # login(request, authenticate(username="dva",password="dva"))

    if path=='index':
        weibos = getWeiboShown(request.user)
        # userinfo = getUserinfo(request.user)
        competes = getCompeteInfo()
        compete3 = competes[:min(3, len(competes))]
        template = loader.get_template('PC_mainPage.html')
        context = {
            'weibos' : weibos,
            # 'userinfo' : userinfo,
            'competes': compete3,
        }
        return HttpResponse(template.render(context, request))
    if path=='transfer':
        template = loader.get_template('PC_tranPage.html')
        context = {}
        return HttpResponse(template.render(context, request))
    if path=='compete':
        template = loader.get_template('PC_competePage.html')
        competes = getCompeteInfo()
        compete4 = competes[:min(4, len(competes))]
        context = {
            'competes': competes,
            'compete4': compete4,
        }
        return HttpResponse(template.render(context, request))
    if path=='compete1':
        id = request.GET.get('id', '')
        alert = request.GET.get('alert', '')
        try:
            id = int(id)
        except:
            return HttpResponse('Bad id.')
        template = loader.get_template('PC_competePage_inner.html')
        competes = getCompeteInfo()
        comptest = getCompeteAtt(request.user, id)
        thai = competes[0]
        default_desc = request.user.username + "的参赛作品，请多多支持。"
        default_title = request.user.username + "的作品"
        pics = getPics(id)
        pictest = getPicTest(request.user, id)
        for compete in competes:
            if compete["id"]==id:
                thai = compete
                competes.remove(compete)
        context = {
            'id': id,
            'alert': alert,
            'thai': thai,
            'competes': competes,
            'comptest': comptest,
            'pictest': pictest,
            'pics': pics,
            'default_desc': default_desc,
            'default_title': default_title,
        }
        return HttpResponse(template.render(context, request))
    if path=='compete2':
        id = request.GET.get('id', '')
        try:
            id = int(id)
        except:
            print('### BAD ID!!')
            return HttpResponseRedirect('/s/compete1?id=1')
        if not request.user.username:
            return HttpResponseRedirect('/s/compete1?id='+str(id)+'&alert=请先登录再报名！')
        if getPicTest(request.user, id):
            return HttpResponseRedirect('/s/compete1?id='+str(id)+'&alert=已提交作品，不能取消报名。')
        doCompeteAtt(request.user, id)
        return HttpResponseRedirect('/s/compete1?id='+str(id))
    if path=='compete3':
        id = request.POST.get('id', '')
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')
        pic = request.FILES.get("pic")
        try:
            id = int(id)
            comp = Competition.objects.get(id=id)
        except:
            print('### BAD ID!!')
            return HttpResponseRedirect('/s/compete1?id=1')
        if not request.user.username:
            return HttpResponseRedirect('/s/compete1?id='+str(id)+'&alert=请先登录再提交作品！')
        if not getCompeteAtt(request.user, id):
            return HttpResponseRedirect('/s/compete1?id='+str(id)+'&alert=未报名比赛，无法提交作品。请先报名。')
        if not pic:
            return HttpResponseRedirect('/s/compete1?id='+str(id)+'&alert=上传图片失败！是否未选择图片？')
        random_name = str(int(time.time())%44567890)
        filename = random_name + os.path.splitext(pic.name)[1]
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        with open(filepath ,"wb") as fPic:
            for chunk in pic.chunks():
                fPic.write(chunk)
        compPic = CompPic(author=request.user,
                          comp=comp,
                          title=title,
                          desc=desc,
                          pic=filename,
                          )
        compPic.save()
        print('SAVED')
        return HttpResponseRedirect('/s/compete1?id='+str(id))
    if path=='my':
        weibos = getWeiboShown(request.user)
        template = loader.get_template('PC_myPage.html')
        userinfo = getUserinfo(request.user)
        pics = getMyPics(request.user, 3)
        pic_count = getPicCount(request.user)
        context = {
            'weibos' : weibos,
            'userinfo': userinfo,
            'pics': pics,
            'pic_count': pic_count,
        }
        return HttpResponse(template.render(context, request))
    if path=='mypic':
        template = loader.get_template('PC_myPage_allPic.html')
        userinfo = getUserinfo(request.user)
        pics = getMyPics(request.user)
        pic_count = getPicCount(request.user)
        picss = []
        for i in range(0, len(pics), 4):
            picss.append({'x':pics[i:min(i+4, len(pics))]})
        context = {
            'userinfo': userinfo,
            'picss': picss,
            'pic_count': pic_count,
        }
        return HttpResponse(template.render(context, request))
    elif path=='dotran':
        return transfer(request)

    return HttpResponse('No Page Here.')

# '/'目录，显示主页
def showMainPage(request):
    logging.info('Accessing Page / with showMainPage')
    return HttpResponseRedirect('/s/index')


# '/<path>'目录，一般是请求资源或者静态网页，直接分类别发送
def showPath(request, path):
    # logging.info('Accessing Page /%s with showPath'%(path))
    if path=='admin':
        return HttpResponseRedirect('admin/')

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

def showMediaT(request, path):
    if path.endswith('jpg') or path.endswith('jpeg'):
        with open(os.path.join(settings.TRANSFER_OUTPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpeg")

    if path.endswith('png'):
        with open(os.path.join(settings.TRANSFER_OUTPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/png")

    if path.endswith('gif'):
        with open(os.path.join(settings.TRANSFER_OUTPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/gif")

        
def showMediaT2(request, path):
    if path.endswith('jpg') or path.endswith('jpeg'):
        with open(os.path.join(settings.TRANSFER_INPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpeg")

    if path.endswith('png'):
        with open(os.path.join(settings.TRANSFER_INPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/png")

    if path.endswith('gif'):
        with open(os.path.join(settings.TRANSFER_INPUT,path), mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/gif")