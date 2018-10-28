
<<<<<<< HEAD
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

def follow(user,to_id):
#    current_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    to_user = User.objects.get(to_id)
    Follow.objects.create(follower=user,following=to_user,build_date=datetime.datetime.now())

def showDetials(user):


