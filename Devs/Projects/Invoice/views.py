#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Invoice.Views.py - Ver.3.5.5 Update:2018.03.14" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
# from django.http import HttpResponse
from Finance.models import Items_Test
from .forms import MyForm


def index(request):
	# return HttpResponse("Invoice Page!! Welcome to Devs.MatsuoStation.Com!")
	items = Items_Test.objects.all().order_by('uid')

	return render(request, 'invoice.html',
		{
			# 'names' : Name_Test.objects.all(),
			# 'Yuki'	: 'Yuki',
			'items'	: items,
		}
	)

def form_test(request):
	form = MyForm()

	return render(request, 'form.html',
		{
			'form'	: form,
		}
	)
