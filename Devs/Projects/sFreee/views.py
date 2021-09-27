#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.sFreee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.sFreee.Views.py - Ver.3.93.2 Update:2021.08.27" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

### Google Apps Script ###
def GAS(request):
	return HttpResponse("Hello sFreee/GAS/ You're at the Google Apps Script.")

### Default ###
def index(request):
	return HttpResponse("Hello RDS to CSV sFreee/Index.py. You're at the Index.")
