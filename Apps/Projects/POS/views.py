#//+------------------------------------------------------------------+
#//|                          VerysVeryInc.Python3.Django.POS.Wsgi.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Django.POS.Views.py - Ver.3.0.2 Update:2018.03.07" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello POS.py. You're at the POS index.")
