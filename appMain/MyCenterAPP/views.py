import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from ShadowInk import settings
from .models import *
import datetime
import random
import os
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


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

def follow(user,to_user):
#    current_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    Follow.objects.create(follower=to_user.personaldetails,following=user.personaldetails)

def getDetails(user):
    details = PersonalDetails.objects.get(user)

    return {
        'avatar' : details.avatar,
        'phone'  : details.phone,
        'bg_img' : details.bg_img,
        'introduction' : details.introduction,
        'address' : details.address,
    }

def showPages(request,path):
    logging.info('Accessing Page /%s with MyCenter.showPages'%(path))

    userinfo = getUserinfo(request.user)

    if not request.user.is_authenticated:
        result = {
            'success': 'False',
            'message': '登录状态错误。',
        }
        return HttpResponse(json.dumps(result))

    if path=='index':
        template = loader.get_template('MyCenter.html')
        details = getUserinfo(request.user)
        return HttpResponse(template.render(details,request))

    if path=='following':
        myFollowing = PersonalDetails.objects.get(request.user).following_set()
        myFollower = request.user.personaldetails.follower_set()
        logging.info(myFollowing)
        logging.info(myFollower)

