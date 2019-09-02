#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|       "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.2 Update:2019.09.02" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def Uriage(request):
	return HttpResponse("Hello Uriage.Py3 You're at the Uriage.")

def index(request):
	return HttpResponse("Hello Freee.Py3 You're at the Index.")
