#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.FreeeAPI.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.FreeeAPI.Views.py - Ver.3.50.2 Update:2020.05.17" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse


def Test(request):
	return HttpResponse("Hello Test.py. You're at the Test.")

def index(request):
	return HttpResponse("Hello FreeeAPI.py. You're at the Index.")
