#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.Py3PDF.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Py3PDF.Views.py - Ver.3.60.1 Update:2020.06.06" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello Py3PDF.py. You're at the Index.")
