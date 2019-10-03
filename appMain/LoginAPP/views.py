# -*- coding:utf-8 -*-

import logging
import json

from django.contrib.auth.models import User
from django.http import *
from django.template import loader
from django.contrib.auth import login, logout

import random
from ShadowInk import settings, mysqlConnector
from qcloudsms_py import SmsSingleSender

from MyCenterAPP.models import PersonalDetails

logger = logging.getLogger(__name__)

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
            checkResult = mysqlConnector.checkPassword(name, password)
            if not checkResult['success']:
                # 登录失败，失败原因在checkResult['message']中
                template = loader.get_template('loginFail.html')
            else :
                # 登陆成功，成功提示也在...中
                template = loader.get_template('loginSuccess.html')
                login(request,checkResult['user'])
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
                insertResult = mysqlConnector.insertUser(name, password)
                if insertResult['success']:# 用户注册成功
                    template = loader.get_template('loginFail.html')
                    context = {
                        'HelloMessage': insertResult['message'],
                    }
                else:# 用户注册失败
                    template = loader.get_template('registerFail.html')
                    context = {
                        'HelloMessage': insertResult['message'],
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
            checkResult = mysqlConnector.checkPassword(name, password)
            if not checkResult['success']:
                result = {
                    'success': 'False',
                    'message': '用户名或密码错误',
                }
            else :
                result = {
                    'success': 'True',
                    'message': '登陆成功',
                }
                login(request,checkResult['user'])

        return HttpResponse(json.dumps(result))

    if path=='ajaxRegister':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            test = User.objects.get(username=name)
            logger.info(test)
            result = {
                'success': 'False',
                'message': '用户已存在！',
            }
        except:
            # user = User(username=name, password=password)
            # userDetail = PersonalDetails(user=user,id=user.id)
            # user.save()
            # userDetail.save()
            result = mysqlConnector.insertUser(name, password)
            # login(request, user)
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