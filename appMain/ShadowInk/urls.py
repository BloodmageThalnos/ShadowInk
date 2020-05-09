"""my URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import viewss
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import *
from django.urls import path
from LoginAPP import views as loginViews
from ExploreAPP import views as exploreViews
from WeiboAPP import views as weiboViews
from pytorchDemo import views as pytorchViews
from TexasAPP import views as texasViews
from MainAPP import views as mainViews
from django.conf.urls import static

urlpatterns = [
    path('', mainViews.showMainPage),
    path('admin/', admin.site.urls),
    path('login/<slug:path>', loginViews.showPages),
    path('e/<slug:path>', exploreViews.showPages),
    # path('w/<slug:path>', weiboViews.showPages),
    path('s/<slug:path>', mainViews.showPages),
    # path('texas/<slug:path>', texasViews.showPages),
    path('media/<path:path>', mainViews.showMedia),
    path('transfer_output/<path:path>', mainViews.showMediaT),
    path('static/<path:path>', mainViews.showPath),
    path('<path:path>', mainViews.showPath),
]
