#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.vIndex.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.vIndex.urls.py - Ver.3.80.60 Update:2021.01.07" |
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

app_name = 'vInvoice'
urlpatterns = [
    # path('admin/', admin.site.urls),

    ### /vInovice/ ###
    path('', views.index, name='index'),

    ### /vInvoice/xxx/ ###
    path('<int:nid>/', views.vInvoice_List.as_view(), name='vinvoice_list'),

    ### /vInvoice/PDF/xxx/ ###
    path('PDF/<int:nid>/', views.PDF_List.as_view(), name='pdf_list'),
    ### /vInvoice/PDF/xxx/ ###
    path('PDF20/<int:nid>/', views.PDF20_List.as_view(), name='pdf20_list'),


]
