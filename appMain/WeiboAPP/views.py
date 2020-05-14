# -*- coding:utf-8 -*-

import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login

from ShadowInk import settings
from .models import *
from pytorchDemo.models import *
from MainAPP.models import *

import random
import os
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def getMyPics(user, max_cnt=0):
    if not user.username:
        return []
    pics = []
    myPics = MyPic.objects.all()
    for myPic in myPics:
        if myPic.author.username == user.username:
            pics.append({
                'a': myPic.picBefore,
                'b': myPic.picAfter
            })
        if max_cnt and len(pics)>=max_cnt:
            break
    while max_cnt and len(pics)<max_cnt:
        pics.append({
            'a': 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D',
            'b': 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D'
        })
    return pics

def getPicCount(user):
    if not user.username:
        return 0
    ans = 0
    myPics = MyPic.objects.all()
    for myPic in myPics:
        ans += 1
    return ans

def getCompeteRealCount(id):
    return CompAtt.objects.filter(comp__id=id).count()

def getCompeteInfo():
    competes = []
    datas = Competition.objects.all()
    for data in datas:
        competes.append({
            'id': data.id,
            'pic': data.pic,
            'title': data.title,
            'desc': data.desc,
            'att_cnt': data.att_cnt + getCompeteRealCount(data.id),
            'start_time': data.start_time,
        })
    return competes

def doCompeteAtt(user, id):
    if not user.username:
        return
    comptest = CompAtt.objects.filter(comp__id=id, user=user)
    print('COMPTEST', comptest)
    if not comptest:
        print('SAVE')
        comp = Competition.objects.get(id=id)
        test = CompAtt(user=user, comp=comp)
        test.save()
    else:
        print('NOSAVE')
        comptest[0].delete()

# return 0/1
def getCompeteAtt(user, id):
    if not user.username:
        return 0
    comptest = CompAtt.objects.filter(comp__id=id, user=user)
    print('COMPTEST', comptest)
    return 1 if comptest else 0

def getPics(id):
    comppics = CompPic.objects.filter(comp__id=id)
    pics = []
    for comppic in comppics:
        pics.append({
            'username': comppic.author.username,
            'create_time': comppic.create_time,
            'upload_time': comppic.upload_time,
            'id': comppic.id,
            'desc': comppic.desc,
            'title': comppic.title,
            'url': '/media/'+comppic.pic,
        })
    return pics

def getPicTest(user, id):
    if not user.username:
        return 0
    pictest = CompPic.objects.filter(comp__id=id, author=user)
    print('PICTEST', pictest)
    return 1 if pictest else 0

def getWeiboShown(user):
    weibos = []
    blogs = Mblog.objects.all()
    for blog in blogs:
        thumbed = False
        if user.is_authenticated:
            try: user.blog_thumb_set.all().get(id=blog.id)
            except: pass
            else: thumbed = True
        tcount = blog.thumb.count()
        comments = blog.comment_blog_set.all()
        comment_set = []
        i = 1
        for comment in comments:
            comment_set.append({
                'num': i,
                'val': comment.content,
                'author': comment.author,
            })
            i+=1
        weibos.append({
            'blog':blog,
            'pics':blog.blog_files_set.all(),
            'thumbed':thumbed,
            'thumbCount':tcount,
            'comments':comment_set,
            'commentCount':len(comment_set),
        })
    return weibos

def getUserinfo(user):
    if user.is_authenticated:
        return {
            'name':user.username,
            'login':True,
        }
    else:
        return {
            'name':'',
            'login':False,
        }

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with weibo.showPages'%(path))

    if path=='index':
        weibos = getWeiboShown(request.user)
        userinfo = getUserinfo(request.user)
        template = loader.get_template('weibo.html')
        context = {
            'weibos' : weibos,
            # 'userinfo' : userinfo,
        }
        return HttpResponse(template.render(context, request))

    if path=='thumbWeibo':
        if not request.user.is_authenticated:
            result = {
                'success' : 'False',
                'message' : '登录状态错误。'
            }
            return HttpResponse(json.dumps(result))
        user = request.user
        id = request.POST.get("id")
        action = request.POST.get("action")
        try:
            blog = Mblog.objects.get(id = int(id))
            if action == 'true':
                ret = blog.thumb.add(user)
            else:
                ret = blog.thumb.remove(user)
        except Exception as e:
            result = {
                'success': 'False',
                'message': '内部错误：%s' % e
            }
            return HttpResponse(json.dumps(result))
        result = {
            'success' : 'True',
            'message' : '点赞成功！' if action=='true' else '取消成功！'
        }
        return HttpResponse(json.dumps(result))

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
        if not request.user.is_authenticated:
            result = {
                'success' : 'False',
                'message' : '登录状态错误，请登录后再发表。'
            }
            return HttpResponse(json.dumps(result))
        user = request.user
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

    if path=='commentWeibo':
        if not request.user.is_authenticated:
            result = {
                'success' : 'False',
                'message' : '登录状态错误。'
            }
            return HttpResponse(json.dumps(result))
        user = request.user
        id = request.POST.get("id")
        content = request.POST.get("content")
        try:
            blog = Mblog.objects.get(id = int(id))
            comment = MblogComment(author=user, blog=blog, refer=None, content=content)
            comment.save()
        except Exception as e:
            result = {
                'success': 'False',
                'message': '内部错误：%s' % e
            }
            return HttpResponse(json.dumps(result))
        result = {
            'success' : 'True',
            'message' : '评论成功！'
        }
        return HttpResponse(json.dumps(result))


    return HttpResponse('No Page Here.')
