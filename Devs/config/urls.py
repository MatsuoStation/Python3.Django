#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.config.urls.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Django.cnf.urls.py - Ver.3.12.2 Update:2018.07.24" |
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
from django.contrib import admin
# (Def.OK) from django.urls import path

### MatsuoStatino.Com ###
from django.urls import include, path

urlpatterns = [
	### MatsuoStation.Com ###
	path('', include('Projects.Index.urls')),
    path('Finance/', include('Projects.Finance.urls')),
	path('Invoice/', include('Projects.Invoice.urls')),
    path('SS/', include('Projects.SS.urls')),
    path('LPG/', include('Projects.LPG.urls')),

	### Config ###
	path('admin/', admin.site.urls),
]
