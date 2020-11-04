#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.nIndex.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.nIndex.Views.py - Ver.3.70.2 Update:2020.11.04" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def Oauth(request):
	return HttpResponse("Hello Oauth.3.0")

def index(request):
	return HttpResponse("Hello nIndex.py. You're at the nIndex.")
