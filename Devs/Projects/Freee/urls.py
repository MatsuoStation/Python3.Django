#//+------------------------------------------------------------------+
#//|                        VerysVeryInc.Python3.Django.Freee.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|        "VsV.Py3.Dj.Freee.urls.py - Ver.3.30.2 Update:2019.10.15" |
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

app_name = 'Freee'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    ### 現金単価 ###
    path('CashUriage/', views.CashUriage, name='cashuriage'),
    path('CashUriage/<int:yid>/', views.CashUriage_List.as_view(), name='cashuriage_list'),


    ### 売上高 ###
    path('Uriage/', views.Uriage, name='uriage'),
    path('Uriage/<int:yid>/', views.Uriage_List.as_view(), name='uriage_list'),
    path('Uriage_CSV/', views.Uriage_Get, name='uriage_get'),
    path('Uriage_CSV/<int:yid>/', views.Uriage_CSV.as_view(), name='uriage_csv'),
]
