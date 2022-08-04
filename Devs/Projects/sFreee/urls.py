#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.sFreee.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.sFreee.urls.py - Ver.3.93.31 Update:2022.06.11" |
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

app_name = 'sFreee'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    ### /sFreee/ ###
    path('GAS/', views.GAS.as_view(), name='GAS'),
    path('GAS/<mdate>/', views.GAS.as_view(), name='GAS_MD'),
    path('GAS_2107/', views.GAS_2107.as_view(), name='GAS_2107'),
    path('GAS_2107/<mdate>/', views.GAS_2107.as_view(), name='GAS_2107_MD'),
]
