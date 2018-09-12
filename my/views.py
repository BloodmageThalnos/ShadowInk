from django.http import HttpResponse
from html import escape

def showPages(request, path):
    print("LOGGING:_____________" + str(request.POST))
    
    url_begin='''
    <html>
    <meta http-equiv="Refresh" content="3; url=/my.html"/>
    <h1>
    你输入的用户名和密码是！
    '''
    
    url_end='''
    </h1>
    </html>
    '''
    
    return HttpResponse(url_begin+str(request.POST)[13:-2]+url_end)

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