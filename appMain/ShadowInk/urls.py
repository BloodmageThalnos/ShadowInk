"""my URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
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
<<<<<<< HEAD
=======
from WeiboAPP import views as weiboViews
>>>>>>> 3fc418e993355769c4672d5bb596459edb822a89
from pytorchDemo import views as pytorchViews
from django.conf.urls import static

urlpatterns = [
    path('', loginViews.showMainPage),
    path('admin/', admin.site.urls),
    path('media/<path:path>', loginViews.showMedia),
    path('login/<slug:path>', loginViews.showPages),
    path('static/<path:path>', loginViews.showPath),
    path('e/<slug:path>', exploreViews.showPages),
    path('p/<slug:path>', pytorchViews.showPages),
<<<<<<< HEAD
=======
    path('w/<slug:path>', weiboViews.showPages),
>>>>>>> 3fc418e993355769c4672d5bb596459edb822a89
    path('<path:path>', loginViews.showPath),
]
