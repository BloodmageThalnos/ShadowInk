from django.http import HttpResponse
from html import escape

def showMainPage(request, path):
    with open('./MainPage/login.html', encoding='UTF-8') as f:
        html = f.read()
    return HttpResponse(html)

def showPages(request, path):
    if path
    
    return None

def showPath(request, path):
    #  print('Debug  ' + path)
    
    if path.endswith('jpg'):
        with open('./MainPage/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpg")
        
    if path.endswith('ico'):
        with open('./MainPage/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/x-icon")
        
    if path.endswith('css'):
        with open('./MainPage/'+path, encoding='UTF-8') as f:
            html = f.read()
        return HttpResponse(html, content_type="text/css")
        
    with open('./MainPage/'+path, encoding='UTF-8') as f:
        html = f.read()
    return HttpResponse(html)