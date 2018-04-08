#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.Invoice.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Invoice.urls.py - Ver.3.5.16 Update:2018.04.08" |
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

app_name = 'Invoice'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('', views.Index_List.as_view(), name='index'),
    # re_path(r'(?P<uid>\d+)/$', views.Invoice_List.as_view(), name='invoice_list')
    # (Def.OK)
    path('<int:nid>/', views.Invoice_List.as_view(), name='invoice_list'),
    # path('<int:nid>/<int:deadline>', views.Invoice_List.as_view(), name='invoice_list_deadine'),
    # path('<int:nid>&dl=<int:deadline>/', views.Invoice_List.as_view(), name='invoice_list_get_deadline'),
    # path('<int:lastday>/', views.Invoice_List.as_view(), name='invoice_lastday'),
    # path('<int:nid>/', views.form_invoice, name='form_invoice')
    # path('form/', views.form_name, name='form_name')
    # path('form/', views.form_test, name='form_test')
    # path('<int:nid>/page<int:page>dl<int:deadline>', views.Invoice_List.as_view(), name='inovice_list_paginated'),
    # path('<int:lastday>/page<int:page>', views.Invoice_List.as_view(), name='inovice_list_lastday_paginated'),
    # (NG) path('<int:nid>/page<int:page>', PaginatedView.as_view()),
]
