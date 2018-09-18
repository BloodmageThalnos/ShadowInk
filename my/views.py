# -*- coding:utf-8 -*-

from django.http import *
from django.template import loader
import logging
import json
import random
from . import main
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

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
        vcode = request.POST.get('vcode')
        context = {}
        if name == None and password == None:
            template = loader.get_template('register.html')
        else:
            # 如果验证码错误
            if vcode != request.session.get('vcode',''):
                template = loader.get_template('registerFail.html')
                context = {
                    'HelloMessage': '验证码错误！请重新输入，或者尝试重新发送。',
                }
            # 尝试向数据库中插入用户，并返回成功与否
            elif not main.insertUser(name, password):
                template = loader.get_template('registerFail.html')
                context = {
                    'HelloMessage': '用户已存在！请重新输入用户名。',
                }
            # 用户注册成功
            else :
                template = loader.get_template('loginFail.html')
                context = {
                    'HelloMessage': '注册成功！请登录。',
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
        pass
        
    if path=='eat':
        user_list = main.getUsers()
        template = loader.get_template('back.html')
        context = {
            'user_list' : user_list,
        }
        return HttpResponse(template.render(context, request))

    if path=='test':
        return HttpResponse('Ok')
        
    if path=='sendSMS':
        phone_number = request.POST.get("phone_number")
        identify_code = str(random.randint(1000,9999))
        request.session['vcode'] = identify_code
        logging.info(phone_number + " , " + identify_code)
        result = {}
        
        
        appid = 1400143065
        appkey = "5299b5d8357ef27f451132f858784a6e"
        phone_numbers = [phone_number]
        template_id = 196454
        sms_sign = "小司机科技"
        ssender = SmsSingleSender(appid, appkey)
        params = [identify_code]
        result = ssender.send_with_param(86, phone_numbers[0],
            template_id, params, sign=sms_sign, extend="", ext="")
        logging.info(result)
        
        
        return HttpResponse(json.dumps(result))
        
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
    
    