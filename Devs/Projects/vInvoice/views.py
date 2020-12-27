#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.5 Update:2020.12.27" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from datetime import datetime

from .forms import NameForm
from .deadline import DeadLine
from .db_vinvoice import DB_vInvoice
from Finance.models import Invoice_Test20, Name_Test20


### vInvoice_List ###
class vInvoice_List(ListView):
	model = Name_Test20
	form_class = NameForm
	template_name = 'vlist.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post )
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Search : g_code ##
		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		## DeadLine : Setup ##
		dd_list = list()

		## * try: * dl = Ture ##
		try:
			dl = self.request.GET.get('dl', '')
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlstr.day 		# DeadLine : Day
			dld, dlm = DeadLine(dd, dlstr)

			'''
			if dd == 20 or dd == 25:
				dld = dlstr + timedelta(days=1) - relativedelta(months=1)
				dlm = dlstr + timedelta(days=1) - timedelta(microseconds=1)
				bld = dld - relativedelta(months=1)
				blm = dlm - relativedelta(months=1)
			else:
				dt = dlstr - relativedelta(months=1)
				dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
				dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)
				bld = dt - timedelta(days=dt.day) + timedelta(days=1)
				blm = bld + relativedelta(months=1) - timedelta(microseconds=1)
			'''

			## DB : Setup ##
			names, IVs = DB_vInvoice(self, dld, dlm)

			'''
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
			'''

			## Cash Income : Total ##
			incash_list = list()
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception : %s" % e)

			## DB : Setup ##
			dld = 'null'
			dlm = 'null'
			names, IVs = DB_vInvoice(self, dld, dlm)

			'''
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
			'''

		for name in names:
			context['names'] = name.g_code.name

		return context

### Index(request) ###
def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post)
	else:
		form = NameForm()
	return render(request, 'vInvoice.html', {'form': form})

	# return HttpResponse("Hello vInvoice/view.py. You're at the vInvoice.")
