# -*- coding:utf-8 -*-

import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
<<<<<<< HEAD
import settings
=======
from ShadowInk import settings
>>>>>>> 3220f7581d55e442160d844c5f5075f4ac6bfe7a
from .models import *

import random
import os
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

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
        template = loader.get_template('mainPC.html')
<<<<<<< HEAD

        userinfo = getUserinfo(request.user)
        template = loader.get_template('weibo.html')

=======
        userinfo = getUserinfo(request.user)
        template = loader.get_template('weibo.html')
>>>>>>> 3220f7581d55e442160d844c5f5075f4ac6bfe7a
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
