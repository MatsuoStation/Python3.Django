#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.6 Update:2020.12.28" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .forms import NameForm
from .deadline import DeadLine, DeadLine_List
from .db_vinvoice import DB_vInvoice
from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20


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
			dld, dlm, dlb, dla = DeadLine(dd, dlstr)

			## DB : Setup ##
			names, IVs, lastmonths, BFs = DB_vInvoice(self, dld, dlm)

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = True) ##
			try:
				if BFs:
					d_values = BFs
				'''
				if Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid')):
					d_values = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
				'''
				for dmm in dlms:
					for d in d_values:
						dls = DeadLine_List(d, dd, dmm)
						'''
						dv = d.check_day

						if dv == 25:
							if dd >= 25:
								dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
							else:
								dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
						elif dv == 20:
							if dd >= 20:
								dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
							else:
								dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
						else:
							dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) - timedelta(days=1)
						'''

						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds
			except Exception as e:
				print("Exception - views.py/ dl=True /LastDay.Check : %s" % e)

			context['deadlines'] = dl
			context['dlb'] = dlb
			context['dla'] = dla

			'''
			dlb = dlstr + timedelta(days=1) - relativedelta(months=1)
			context['dlb'] = dlb
			dla = dlstr + timedelta(days=1) - timedelta(microseconds=1)
			context['dla'] = dla
			'''
			## End of LastDay : Check (dl = True) ##

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
			names, IVs, lastmonths, BFs = DB_vInvoice(self, "", "")

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = False) ##
			try:
				if BFs:
					d_values = BFs
				'''
				if Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid')):
					d_values = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
				'''
				for dmm in dlms:
					for d in d_values:
						dls = DeadLine_List(d, dd, dmm)
						'''
						dv = d.check_day

						if dv == 25:
							if dd >= 25:
								dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
							else:
								dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
						elif dv == 20:
							if dd >= 20:
								dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
							else:
								dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
						else:
							dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) - timedelta(days=1)
						'''

						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds
			except Exception as e:
				print("Exception - views.py/ dl=False /LastDay.Check : %s" % e)

			context['deadlines'] = dl
			## End of LastDay : Check (dl = False) ##

		## name : Setup ##
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
