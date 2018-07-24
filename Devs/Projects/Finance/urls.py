#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.Finance.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Finance.urls.py - Ver.3.12.1 Update:2018.07.24" |
#//+------------------------------------------------------------------+
"""Devs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

### MatsuoStation.Com ###
from . import views

app_name = 'Finance'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('SHARP/', views.sharp, name='sharp'),
    path('ScanXLS/', views.sxls, name='sxls'),
    path('POS/', views.pos, name='pos'),
    path('InCash/', views.incash, name='incash'),

    # path('MySQL/', views.mysql, name='mysql'),
]
