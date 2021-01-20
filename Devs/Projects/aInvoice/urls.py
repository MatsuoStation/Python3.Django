#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.aInvoice.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.Dj.aInvoice.urls.py - Ver.3.91.2 Update:2021.01.14" |
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

app_name = 'aInvoice'
urlpatterns = [
    # path('admin/', admin.site.urls),

    ### /aInovice/ ###
    path('', views.index, name='index'),

    ### /aInvoice/xxx/ ###
    path('<int:nid>/', views.aInvoice_List.as_view(), name='ainvoice_list'),

    ### /aInvoice/bFreee/ ###
    path('bFreee/', views.bFreee, name='bfreee'),
    path('bFreee/<int:bid>/', views.bFreee_List.as_view(), name='bfreee_list'),
]
