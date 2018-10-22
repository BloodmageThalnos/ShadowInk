# -*- coding:utf-8 -*-

import logging
import json
from django.http import *
from django.template import loader
from django.contrib.auth import login
from ShadowInk import settings
from .models import *

from TexasAPP.holdem_calc import run
from TexasAPP.holdem_functions import Card

logger = logging.getLogger(__name__)

def showPages(request, path):
    if path=='index':
        template = loader.get_template('texas.html')
        return HttpResponse(template.render({}, request))

    if path=='calc':
        cards = request.POST.get("car")
        board = request.POST.get("boa")
        out = request.POST.get("out")
        unknown = request.POST.get("unk")
        exact = request.POST.get("exa")
        num = 45678
        e=(exact=='1')
        c,d,o = [],[],[]
        for card in cards.split('_'):
            a,b=card.split(',')
            c.append((Card(a),Card(b)))
        if board!="":
            for bd in board.split('_'):
                d.append(Card(bd))
        if out!="":
            for outa in out.split('_'):
                o.append(Card(outa))
        if unknown=='on':
            c.append((None,None))
        i,j = run(c,num,d,o,e)
        return HttpResponse(i)

    return HttpResponse('No Page Here.')
