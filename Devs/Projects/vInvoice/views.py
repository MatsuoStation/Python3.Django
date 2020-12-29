#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.10 Update:2020.12.29" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .forms import NameForm
from .Util.deadline import DeadLine, DeadLine_List
# from .db_vinvoice import DB_vInvoice
from .Util.db_vinvoice import DB_vInvoice
from .pdf import fPDF_SS_BackImage
from Finance.models import Name_Test20


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
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=True / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			context['dlb'] = dlb
			context['dla'] = dla
			## End of LastDay : Check (dl = True) ##

			## BANK : Invoice.Format ##
			for bf in BFs:
				fPDF = bf.s_format
				context['fPDF'] = fPDF

				## Invoice.Format : Back.Image - Setup
				fURL = fPDF_SS_BackImage(fPDF)
				context['fURL'] = fURL
			## End of BANK : Invoice.Format ##

			## Cash Income : Total ##
			incash_list = list()
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values

			## Cash Value : Total ##
			total_list = list()

			## Caluculate ##
			try:
				## Select Month ##
				for iv in IVs:
					# 現金関係 or 振込関係
					if iv.s_code.uid == "00000" or iv.s_code.uid == "00002":
						sv = 0
						total_list.append(sv)
					else:
						sv = 0
						total_list.append(sv)

				## Value : Sum ##
				total_values = sum(total_list)

				## Value : Context ##
				context['total_values'] = total_values

			except Exception as e:
				print("Exception - views.py / dl=True / Caluculate  : %s" % e)
			## End of Caluculate ##

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## DB : Setup ##
			names, IVs, lastmonths, BFs = DB_vInvoice(self, "", "")

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = False) ##
			try:
				if BFs:
					d_values = BFs
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=False / LastDay.Check : %s" % e)

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
