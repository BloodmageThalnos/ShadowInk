
import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from appMain.ShadowInk import settings
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

def follow(user,to_id):
#    current_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    to_user = User.objects.get(to_id)
    Follow.objects.create(follower=user,following=to_user,build_date=datetime.datetime.now())

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

    if path=='index':
        userinfo = getUserinfo(request.user)
        template = loader.get_template('MyCenter.html')
        details = getUserinfo(request.user)
        return HttpResponse(template.render(details,request))

