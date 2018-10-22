# -*- coding:utf-8 -*-

import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from appMain.ShadowInk import settings
from .models import *

logger = logging.getLogger(__name__)


def showPages(request, path):
    logging.info('Accessing Page /%s with weibo.showPages'%(path))

    if path=='index':
        pass

    if path=='calc':


    return HttpResponse('No Page Here.')
