#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Dj.Invoice.Views.py - Ver.3.7.11 Update:2018.03.29" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse

from django.views.generic import ListView
from Finance.models import Name_Test, Items_Test, SHARP_Test, Value_Test
from .forms import NameForm
# from .forms import NameForm, MyForm
from Finance.models import Name_Test02, SHARP_Test02

from Finance.models import Invoice_Test10, Name_Test10, Items_Test10, Value_Test10
from Finance.models import Invoice_Test20, Name_Test20


class Invoice_List(ListView):

	model = Name_Test
	# model = SHARP_Test
	form_class = NameForm
	template_name = 'list.html'
	# (OK) context_object_name = "sharptb"
	context_object_name = "nametb"
	# paginate_by = 10

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		lastday_post = request.POST['lastday']
		if form.is_valid():
			return HttpResponseRedirect('/Invoice/%s' % nid_post)

		return render(request, self.template_name, {'form': form})

	'''
	def h_name(self):
		sharps = SHARP_Test.objects.filter(g_code__endswith=self.kwargs.get('nid'))

		for sharp in sharps:
			h_name = Items_Test.objects.all().filter(uid__startswith=sharp.s_code)
		return h_name
	'''

	# def get_queryset(self):
		# uid = self.request.GET.get('uid')
		# uid = self.request.POST.get('uid')

		# (OK) return SHARP_Test.objects.filter(g_code__endswith=self.kwargs.get('nid'))
		# return NAME_Test.objects.filter(uid__endswith=self.kwargs.get('nid'))
		# return SHARP_Test.objects.filter(g_code__endswith=uid)
		# return SHARP_Test.objects.filter(g_code="0104")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = NameForm()
		# context['nid_post'] = request.POST.get('nid')

		# context['nid'] = request.POST['nid']
		# context['post_nid'] = self.NameForm

		# sharps = SHARP_Test02.objects.filter(g_code__uid__endswith='0104')
		# sharps = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid'))
		# (Ver.3.7.3.OK) sharps = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')
		# (Ver.3.7.7.OK) IVs = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code').select_related('s_code')
		IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
		# IVs = Invoice_Test10.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code')
		# names = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# (Ver.3.7.7.OK) names = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')
		names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
		# (Ver.3.7.7.OK) items = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('s_code')
		# items = Invoice_Test20.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('s_code')
		# values = Value_Test10.objects.all().filter(uid="0104", s_code="10100")
		# (Ver.3.7.7.OK) values = Value_Test10.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code="10100")
		# values = Value_Test20.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code="10100")


		for name in names:
			context['names'] = name.g_code.name
		# for name in IVs:
		#	context['names'] = name.g_code.name

		# for item in items:
		#	context['items'] = item.s_code.h_name
		# context['values'] = values

		# for i in IVs:
		#	values = Value_Test10.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code=i.s_code)

		#	for v in values:
		#		context['values'] = v.value



		# for v in values:
		#	context['values'] = v.value



		context['ivs'] = IVs


		'''
		sharps = SHARP_Test.objects.all().filter(
			g_code__endswith=self.kwargs.get('nid'),
		)
		'''

		# (Ver.3.7.3.OK) names = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# names = SHARP_Test02.objects.filter(g_code__uid__startswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# (OK) names = Name_Test02.objects.filter(uid__endswith=self.kwargs.get('nid'))
		# (OK) names = Name_Test.objects.all().filter(uid__endswith=self.kwargs.get('nid'))
		# names = Name_Test.objects.all().filter(uid__startswith="0104")

		# items = Items_Test.objects.all().filter(uid__startswith='1010')
		# items = Items_Test.objects.all().filter(uid__startswith="1020")

		# context['sharps'] = sharps
		# context['names'] = names
		# (Ver.3.7.3.OK) for name in names:
			# context['names'] = name.name
		# (Ver.3.7.3.OK) 	context['names'] = name.g_code.name


		# context['names'] = names

		# items = Items_Test.objects.filter(uid=sharps.objects.filter(s_code))
		# context['items'] = i.h_name

		# (Ver.3.7.3.OK) for sharp in sharps:
			# items = Items_Test.objects.all().filter(uid__startswith='1010')
			# items = Items_Test.objects.all().filter(uid__startswith='10200')
		# (Ver.3.7.3.OK) 	items = Items_Test.objects.filter(uid=sharp.s_code)
		# (Ver.3.7.3.OK) 	for i in items:
		# (Ver.3.7.3.OK) 		context['items'] = i.h_name

		# (Ver.3.7.3.OK) context['sharps'] = sharps
		# context['items'] = items

		#context['h_name'] = self.h_name

		# items = Items_Test.objects.all().filter(uid__startswith="1010")
		# context['s_codes'] = items

		# context['sc'] = Items_Test.objects.filter(uid__startswith="1010")

		return context


def index(request):
	# return HttpResponse("Invoice Page!! Welcome to Devs.MatsuoStation.Com!")

	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/Invoice/%s' % nid_post)

	else:
		form = NameForm()

	return render(request, 'invoice.html', {'form': form})

	# items = Items_Test.objects.all().order_by('uid')
	# names = Name_Test.objects.all().order_by('uid')
	# return render(request, 'invoice.html',
	#	{
	#		# 'names' : Name_Test.objects.all(),
	#		# 'Yuki'	: 'Yuki',
	#		'names' : names,
	#		'items'	: items,
	#	}
	# )


def form_invoice(request, nid):
	# return HttpResponse("You're looking at Form_Invoice %s" % uid)
	forms = get_object_or_404(Name_Test, uid__endswith=nid)
	# forms = get_list_or_404(Name_Test, uid=nid)
	sharps = SHARP_Test.objects.all().filter(g_code__endswith=nid)
	items = Items_Test.objects.all()


	if request.method == 'POST':
		form = NameForm(request.POST)

		if form.is_valid():
			pass

	else:
		form = NameForm()

	return render(request, 'form.html',
		{
			'form'	: form,
			'forms'	: forms,
			'sharps': sharps,
			'items'	: items,
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

''' (Def)
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
'''