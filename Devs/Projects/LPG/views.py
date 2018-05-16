#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Django.LPG.Views.py - Ver.3.11.2 Update:2018.05.16" |
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

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlt.day

			dt = dlt - relativedelta(months=1)
			dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
			dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)

			context['dld'] = dld
			context['dlm'] = dlm

			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'), m_datetime__lte=dlm)
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test20.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')

			context['lms'] = LMs

			### LPG.検針データ ###
			for lm in LMs:
				# 氏名
				for na in NAs:
					names = na.name

				# 日付
				monLPG = datetime.strftime(lm.m_datetime, '%-m')
				dayLPG = datetime.strftime(lm.m_datetime, '%-d')
				context['monLPG'] = monLPG
				context['dayLPG'] = dayLPG

				# ガス使用量
				aLPG = lm.amount

				if aLPG > 0:
					# 商品コード
					s_code = lm.s_code

					# ガス料金コード
					for vl in VLs:
						cLPG = vl.s_code

					# 基本料金
					LVs = LPG_Value00.objects.all().filter(uid=cLPG)
					for lv in LVs:
						bLPG = lv.base_value

					context['s_code'] = s_code
					context['cLPG'] = cLPG
					context['bLPG'] = bLPG

					context['base_product'] = "基本料金"
					context['product'] = "ガス使用量"
					context['unit_product'] = "(内訳)"

				context['names'] = names
				context['aLPG'] = aLPG


			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG


		### DL : False ###
		except Exception as e:
			print(e, 'LPG/Views - DL.False : error occured')

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
