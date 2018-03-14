#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Dj.Invoice.Views.py - Ver.3.5.10 Update:2018.03.14" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

# Create your views here.
### MatsuoStation.Com ###
# from django.http import HttpResponse

from Finance.models import Name_Test, Items_Test
from .forms import NameForm, MyForm


def index(request):
	# return HttpResponse("Invoice Page!! Welcome to Devs.MatsuoStation.Com!")
	items = Items_Test.objects.all().order_by('uid')
	names = Name_Test.objects.all().order_by('uid')

	return render(request, 'invoice.html',
		{
			# 'names' : Name_Test.objects.all(),
			# 'Yuki'	: 'Yuki',
			'names' : names,
			'items'	: items,
		}
	)

def form_invoice(request, nid):
	# return HttpResponse("You're looking at Form_Invoice %s" % uid)
	forms = get_object_or_404(Name_Test, uid__endswith=nid)
	# forms = get_list_or_404(Name_Test, uid=nid)

	return render(request, 'form.html',
		{
			'forms'	: forms,
		}
	)


def form_name(request):
	names = Name_Test.objects.all().order_by('uid')

	if request.method == 'POST':
		form = NameForm(request.POST)

		if form.is_valid():
			pass

	else:
		form = NameForm()

	return render(request, 'form.html',
		{
			'names'	: names,
			'form'	: form,
		}
	)


def form_test(request):
	if request.method == "POST" :
		form = MyForm(data=request.POST)	# 受け取ったPOSTデータを渡す
		if form.is_valid():					# 受け取ったデータの正当性確認
			pass							# 正しいデータを受け取った場合の処理
	else:
		form = MyForm()

	# form = MyForm()

	return render(request, 'form.html',
		{
			'form'	: form,
		}
	)
