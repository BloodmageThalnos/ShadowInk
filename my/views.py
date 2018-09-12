from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# '/'目录，显示主页
def showMainPage(request, path):
    logging.info('Accessing Page /%s with showMainPage'%(path))
    with open('./MainPage/login.html', encoding='UTF-8') as f:
        html = f.read()
        return HttpResponse(html)

def showPages(request, path):
    logging.info('Accessing Page /%s with showPages'%(path))
    if path=='explore':
        with open('./MainPage/my.html', encoding='UTF-8') as f:
            html = f.read()
            return HttpResponse(html)
        
    if path=='login':
        
        
        return HttpResponse(url_begin+str(request.POST)[13:-2]+url_end)
    return None

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