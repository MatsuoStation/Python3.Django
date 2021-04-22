#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.cFreee.Views.py - Ver.3.92.1 Update:2021.04.22" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello cFreee/Index.py. You're at the Index.")
