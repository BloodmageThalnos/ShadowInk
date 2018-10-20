# -*- coding:utf-8 -*-

import logging
import json

from django.contrib.auth.models import User
from django.http import *
from django.template import loader
from django.contrib.auth import login, logout, authenticate

import random
from ShadowInk import settings
from qcloudsms_py import SmsSingleSender

logger = logging.getLogger(__name__)

# '/'目录，显示主页
def showMainPage(request):
    logging.info('Accessing Page / with showMainPage')
    return HttpResponseRedirect('/login/login')

# '/<slug>'目录，分别处理，对于未知的slug返回none
def showPages(request, path):
    logging.info('Accessing Page /%s with login.showPages'%(path))

    if path=='login':
        name = request.POST.get('name')
        password = request.POST.get('password')
        if name == None and password == None:
            # 未提交任何请求，或者用户名密码未输入
            template = loader.get_template('login.html')
            context = {}
        else:
            logger.info('Checking password, name:%s, password:%s' % (name, password))
            user = None
            if name == None:
                checkResult = {'success': False, 'message': '用户名不能为空！'}
            elif password == None:
                checkResult = {'success': False, 'message': '密码不能为空！'}
            else:
                user = authenticate(username=name, password=password)
                if user == None:
                    checkResult = {'success': False, 'message': '用户名或密码错误！'}
                else:
                    checkResult = {'success': True, 'message': '欢迎回来，%s，好久不见了！' % (name)}
            if not checkResult['success']:
                # 登录失败，失败原因在checkResult['message']中
                template = loader.get_template('loginFail.html')
            else :
                # 登陆成功，成功提示也在checkResult['message']中
                template = loader.get_template('loginSuccess.html')
                login(request,user)
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
            # 如果验证码错误 (pass是测试用的后门)
            if vcode != 'pass' and vcode != request.session.get('vcode',''):
                template = loader.get_template('registerFail.html')
                context = {
                    'HelloMessage': '验证码错误！请重新输入，或者尝试重新发送。',
                }
            # 尝试向数据库中插入用户，并返回成功与否
            else:
                user = User.objects.create_user(username=name, password=password, email=None)
                user.save()
                template = loader.get_template('loginFail.html')
                context = {
                    'HelloMessage': '注册成功，请登录！',
                }
        return HttpResponse(template.render(context, request))

    if path=='ajaxLogin':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if name == None or password == None:
            result = {
                'success': 'False',
                'message': '请填写用户名和密码',
            }
        else:
            logger.info('Checking password, name:%s, password:%s' % (name, password))
            user = authenticate(username=name, password=password)
            if user == None:
                result = {'success': 'False', 'message': '用户名或密码错误！'}
            else:
                result = {'success': 'True', 'message': '登陆成功！'}
                login(request,user)
        return HttpResponse(json.dumps(result))

    if path=='ajaxLogout':
        if request.POST.get('logout')!='sure': return None
        if not request.user.is_authenticated:
            result = {
                'success': 'False',
                'message': '已经注销或根本没有登录，请刷新重试。',
            }
        else:
            logout(request)
            result = {
                'success': 'True',
                'message': '注销成功！！！太棒啦',
            }
        return HttpResponse(json.dumps(result))

    if path=='sendSMS':
        phone_number = request.POST.get("phone_number")
        identify_code = str(random.randint(1000,9999))
        request.session['vcode'] = identify_code
        logging.info("Phone number: " + phone_number + " , Identify_code: " + identify_code)
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
        return HttpResponse(html, content_type="application/font-woff")

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
    logging.info('Accessing Page /%s with showPath'%(path))

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
