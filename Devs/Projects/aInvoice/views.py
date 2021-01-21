#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.aInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.aInvoice.Views.py - Ver.3.91.3 Update:2021.01.21" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime, timedelta

from .forms import NameForm, BankForm
from Finance.models import Name_Test20, Bank_Test20
from .Util.db_ainvoice import DB_aInvoice
from .Util.deadline import DeadLine, DeadLine_List
from .Util.freee_api import Get_A_Token, Freee_Account


### Freee_API ###
## bFreee ##
def bFreee(request):
	if request.method == 'POST':
		form = BankForm(request.POST)
		bid_post = request.POST['bid']
		if form.is_valid():
			return HttpResponseRedirect('/aInvoice/bFreee/%s' % bid_post)
	else:
		form = BankForm()
	return render(request, 'blist.html', {'form': form})


## bFreee_List ##
class bFreee_List(ListView):
	model = Bank_Test20
	form_class = BankForm
	template_name = 'blist.html'
	context_object_name = "banktb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		bid_post = request.POST['bid']
		if form.is_valid():
			return HttpResponseRedirect('/aInvoice/bFreee/%s' % bid_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Serch : Bank_Code ##
		context['form'] = BankForm()
		context['bid'] = self.kwargs.get('bid')

		## PlusFree.API : Setup ##
		a_code, r_code, company_id = Freee_Account(self)
		# a_code, r_code = Get_A_Token("", "4d853fec089e8717efef31f9f60261707dcefbc7ef065c40c495b548b680d61c")
		context['a_code'] = a_code
		context['r_code'] = r_code
		context['company_id'] = company_id

		return context


### aInvoice_List ###
class aInvoice_List(ListView):
	model = Name_Test20
	form_class = NameForm
	template_name = 'alist.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/aInvoice/%s' % nid_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Search : g_code ##
		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		## DeadLine : Setup ##
		# dd_list = list()

		## * try: * dl = Ture ##
		try:
			dl = self.request.GET.get('dl', '')
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlstr.day  # DeadLine : Day
			dld, dlm, dlb, dla, bld, blm = DeadLine(dd, dlstr)

			## DB : Setup ##
			names, SnP, lastmonths, BFs = DB_aInvoice(self, dld, dlm, bld, blm)

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			try:
				if BFs:
					d_values = BFs
				dd_list, dv = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
				context['dv'] = dv
			except Exception as e:
				print("Exception - views.py / dl=True / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			context['dlb'] = dlb
			context['dla'] = dla
			## End of LastDay : Check (dl = True) ##

		## * try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## DB : Setup ##
			names, SnP, lastmonths, BFs = DB_aInvoice(self, "", "", "", "")

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = False) ##
			try:
				if BFs:
					d_values = BFs
				dd_list, dv = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
				context['dv'] = dv
			except Exception as e:
				print("Exception - views.py / dl=False / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			## End of LastDay : Check (dl = False) ##

		## name : Setup ##
		for n in names:
			context['names'] = n.name

		## Paginator : Setup ##
		paginator = Paginator(SnP, 30)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1
		try:
			SnP = paginator.page(page)
		except(EmptyPage, InvalidPage):
			SnP = paginator.page(1)
		context['snp'] = SnP

		return context

### Index(request) ###
def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/aInvoice/%s' % nid_post)
	else:
		form = NameForm()
	return render(request, 'aInvoice.html', {'form': form})

	# return HttpResponse("Hello aInvoice/view.py. You're at the aInvoice.")