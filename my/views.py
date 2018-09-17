# -*- coding:utf-8 -*-

from django.http import *
from django.template import loader
import logging
from . import main

logger = logging.getLogger(__name__)

# '/'目录，显示主页
def showMainPage(request):
    logging.info('Accessing Page / with showMainPage')
    return HttpResponseRedirect('/login')

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with showPages'%(path))
    if path=='explore':
        with open('./MainPage/my.html', encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html)
        
    if path=='login':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name == None and password == None:
            template = loader.get_template('login.html')
            context = {}
        else:
            checkResult = main.checkPassword(name, password)
            if checkResult['success']:
                template = loader.get_template('loginSuccess.html')
            else :
                template = loader.get_template('loginFail.html')
            context = {
                'HelloMessage': checkResult['message'],
            }
        return HttpResponse(template.render(context, request))
    
    if path=='register':
        name = request.POST.get('name')
        password = request.POST.get('password')
        context = {}
        if name == None and password == None:
            template = loader.get_template('register.html')
        else:
            insertResult = main.insertUser(name, password)
            if insertResult:
                template = loader.get_template('loginFail.html')
                context = {
                    'HelloMessage': '注册成功！请登录。',
                }
            else :
                template = loader.get_template('registerFail.html')
                context = {
                    'HelloMessage': '用户已存在！请重新输入用户名。',
                }
        return HttpResponse(template.render(context, request))
        
    if path=='pContent':
        articles = main.getArticles()
        template = loader.get_template('pages/pContent.html')
        context = {
            'articles' : articles
        }
        return HttpResponse(template.render(context, request))
        
    if path=='pPostArticle':
        
        
    if path=='eat':
        user_list = main.getUsers()
        template = loader.get_template('back.html')
        context = {
            'user_list' : user_list,
        }
        return HttpResponse(template.render(context, request))

    if path=='test':
        main.insertArticle(4,'【今日新闻】邢凯笑了','https://gss0.bdstatic.com/7Ls0a8Sm1A5BphGlnYG/sys/portrait/item/450a6a696e5f6d7a3601.jpg','抓拍了一张正在笑的邢凯！就是有点蓝。')
        return HttpResponse('Ok')
        
    return HttpResponse('No Page Here.')

# '/<path>'目录，一般是请求资源或者静态网页，直接分类别发送
def showPath(request, path):
    logging.info('Accessing Page /%s with showPath'%(path))
    
    if path.endswith('jpg'):
        with open('./MainPage/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpg")
        
    if path.endswith('png'):
        with open('./MainPage/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/png")
        
    if path.endswith('ico'):
        with open('./MainPage/image/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/x-icon")
        
    if path.endswith('css'):
        with open('./MainPage/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html, content_type="text/css")
        
    with open('./MainPage/'+path, encoding='UTF-8') as f:
        html = f.read()
    return HttpResponse(html)
    
    