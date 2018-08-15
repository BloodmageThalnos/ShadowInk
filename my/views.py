from django.http import HttpResponse

def show(request, path=''):
    if path.endswith('jpg'):
        with open('./MainPage/'+path, mode="rb") as f:
            html = f.read()
        return HttpResponse(html, content_type="image/jpg")
    with open('./MainPage/'+path, encoding='UTF-8') as f:
        html = f.read()
    return HttpResponse(html)
