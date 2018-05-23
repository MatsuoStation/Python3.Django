#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Python3.Django.LPG.Views.py - Ver.3.11.10 Update:2018.05.23" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import HttpResponse

from django.views.generic import ListView
from .forms import NameForm

from Finance.models import Name_Test20, LPG_Meter00, Bank_Test20, Value_Test20, LPG_Value00
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

jtax = 0.08
ndigits = 0

def tax_v(value):

	values = value * jtax
	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		return int(round(values, 0))
	c = (10 ** d_point) * 2
	return int(round((values * c + 1) / c, 0))

def invalue(values):
	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		return int(round(values, 0))
	c = (10 ** d_point) * 2
	return int(round((values * c + 1) / c, 0))


class LPG_List(ListView):

	model = Name_Test20
	form_class = NameForm
	template_name = 'lpg_list.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect( '/LPG/%s' % nid_post)

		return render(request, self.template_name, {'form': form})


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		dd_list = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')

			# (OK) dd = dlt.day

			# (OK) dt = dlt - relativedelta(months=1)
			# (OK) dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
			# (OK) dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)

			# (OK) context['dld'] = dld
			# (OK) context['dlm'] = dlm
			dlb = dlt + timedelta(days=1) - relativedelta(months=1)
			dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
			context['dlb'] = dlb
			context['dla'] = dla

			# LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'), m_datetime__lte=dlm)
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test20.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')

			context['lms'] = LMs

			### 検針実施日 ###
			try:
				for lm in LMs:
					date00 = lm.m_datetime
					dd00 = lm.m_datetime.day
					date00 = (date00-timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
					dd_list.append(date00)

					if lm.date01:
						date01 = lm.date01
						dd01 = lm.date01.day
						date01 = (date01-timedelta(days=dd01-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date01)
					if lm.date02:
						date02 = lm.date02
						dd02 = lm.date02.day
						date02 = (date02-timedelta(days=dd02-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date02)
					if lm.date03:
						date03 = lm.date03
						dd03 = lm.date03.day
						date03 = (date03-timedelta(days=dd03-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date03)
					if lm.date04:
						date04 = lm.date04
						dd04 = lm.date04.day
						date04 = (date04-timedelta(days=dd04-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date04)
					if lm.date05:
						date05 = lm.date05
						dd05 = lm.date05.day
						date05 = (date05-timedelta(days=dd05-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date05)
					if lm.date06:
						date06 = lm.date06
						dd06 = lm.date06.day
						date06 = (date06-timedelta(days=dd06-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date06)
					if lm.date07:
						date07 = lm.date07
						dd07 = lm.date07.day
						date07 = (date07-timedelta(days=dd07-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date07)
					if lm.date08:
						date08 = lm.date08
						dd08 = lm.date08.day
						date08 = (date08-timedelta(days=dd08-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date08)
					if lm.date09:
						date09 = lm.date09
						dd09 = lm.date09.day
						date09 = (date09-timedelta(days=dd09-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date09)
					if lm.date10:
						date10 = lm.date10
						dd10 = lm.date10.day
						date10 = (date10-timedelta(days=dd10-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date10)
					if lm.date11:
						date11 = lm.date11
						dd11 = lm.date11.day
						date11 = (date11-timedelta(days=dd11-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date11)
					if lm.date12:
						date12 = lm.date12
						dd12 = lm.date12.day
						date12 = (date12-timedelta(days=dd12-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date12)

				dds = sorted(set(dd_list), key=dd_list.index)
				context['dds'] = dds

			except Exception as e:
				print(e, 'LPG/views.py_dds : error occured')

			### 氏名 ###
			for na in NAs:
				names = na.name

			### LPG.検針データ ###


			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG


		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### 検針実施日 ###
			try:
				for lm in LMs:
					date00 = lm.m_datetime
					dd00 = lm.m_datetime.day
					date00 = (date00-timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
					dd_list.append(date00)

					if lm.date01:
						date01 = lm.date01
						dd01 = lm.date01.day
						date01 = (date01-timedelta(days=dd01-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date01)
					if lm.date02:
						date02 = lm.date02
						dd02 = lm.date02.day
						date02 = (date02-timedelta(days=dd02-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date02)
					if lm.date03:
						date03 = lm.date03
						dd03 = lm.date03.day
						date03 = (date03-timedelta(days=dd03-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date03)
					if lm.date04:
						date04 = lm.date04
						dd04 = lm.date04.day
						date04 = (date04-timedelta(days=dd04-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date04)
					if lm.date05:
						date05 = lm.date05
						dd05 = lm.date05.day
						date05 = (date05-timedelta(days=dd05-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date05)
					if lm.date06:
						date06 = lm.date06
						dd06 = lm.date06.day
						date06 = (date06-timedelta(days=dd06-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date06)
					if lm.date07:
						date07 = lm.date07
						dd07 = lm.date07.day
						date07 = (date07-timedelta(days=dd07-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date07)
					if lm.date08:
						date08 = lm.date08
						dd08 = lm.date08.day
						date08 = (date08-timedelta(days=dd08-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date08)
					if lm.date09:
						date09 = lm.date09
						dd09 = lm.date09.day
						date09 = (date09-timedelta(days=dd09-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date09)
					if lm.date10:
						date10 = lm.date10
						dd10 = lm.date10.day
						date10 = (date10-timedelta(days=dd10-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date10)
					if lm.date11:
						date11 = lm.date11
						dd11 = lm.date11.day
						date11 = (date11-timedelta(days=dd11-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date11)
					if lm.date12:
						date12 = lm.date12
						dd12 = lm.date12.day
						date12 = (date12-timedelta(days=dd12-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date12)

				dds = sorted(set(dd_list), key=dd_list.index)
				context['dds'] = dds

			except Exception as e:
				print(e, 'LPG/views.py_dds : error occured')


			### 氏名 ###
			for na in NAs:
				names = na.name

			print(e, 'LPG/Views - DL.False : error occured')

		context['names'] = names

		return context



def index(request):
	# return HttpResponse("Devs.LPG Page!! Welcome to Devs.MatsuoStation.Com!")
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/LPG/%s' % nid_post)

	else:
		form = NameForm()

	return render(request, 'lpg.html', {'form': form})
