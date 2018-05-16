#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Django.LPG.Views.py - Ver.3.11.3 Update:2018.05.16" |
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
					LVs01 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:1]
					for lv in LVs01:
						bLPG = lv.base_value
						taxLPG = tax_v(bLPG)

						# ガス使用料金
						s0 = lv.start_value
						e0 = lv.end_value
						u0 = int(lv.unit)

						if aLPG >= e0:
							v0 = invalue(u0*(e0-s0))
							# v0 = u0 * (e0 - s0)

							t0 = tax_v(v0)
							# values = v0 * jtax
							# d_point = len(str(values).split('.')[1])
							# if ndigits >= d_point:
							#	t0 = int(round(values, 0))
							# c = (10 ** d_point) * 2
							# t0 = int(round((values * c + 1) / c, 0))

							# r0 = infloat(aLPG-e0)
							r0 = e0 - s0

						elif aLPG < s0:
							v0 = int(0)
						else:
							v0 = invalue(u0*(aLPG-s0))
							# v0 = u0 * (aLPG - s0)
							t0 = tax_v(v0)
							# values = v0 * jtax
							# d_point = len(str(values).split('.')[1])
							# if ndigits >= d_point:
							#	t0 = int(round(values, 0))
							# c = (10 ** d_point) * 2
							# t0 = int(round((values * c + 1) / c, 0))
							r0 = aLPG - s0


					LVs02 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:2]
					for lv in LVs02:
						s1 = lv.start_value
						e1 = lv.end_value
						u1 = int(lv.unit)

						if aLPG >= e1:
							v1 = invalue(u1*(e1-e0))
							# v1 = u1 * (e1 - e0)
							t1 = tax_v(v1)
							r1 = e1 - e0

						elif aLPG < s1:
							v1 = int(0)
						else:
							v1 = invalue(u1*(aLPG-e0))
							# v1 = u1 * (aLPG - e0)
							t1 = tax_v(v1)
							r1 =  aLPG - e0

					LVs03 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:3]
					for lv in LVs03:
						s2 = lv.start_value
						e2 = lv.end_value
						u2 = int(lv.unit)

						if aLPG >= e2:
							v2 = invalue(u2*(e2-e1))
							t2 = tax_v(v2)
							r2 = e2-e1

						elif aLPG < s2:
							v2 = int(0)
						else:
							v2 = invalue(u2*(aLPG-e1))
							t2 = tax_v(v2)
							r2 = aLPG - e1

					LVs04 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:4]
					for lv in LVs04:
						s3 = lv.start_value
						e3 = lv.end_value
						u3 = int(lv.unit)

						if aLPG >= e3:
							v3 = invalue(u3*(e3-e2))
							t3 = tax_v(v3)
							r3 = e3-e2

						elif aLPG < s3:
							v3 = int(0)
						else:
							v3 = invalue(u3*(aLPG-e2))
							t3 = tax_v(v3)
							r3 = aLPG - e2

					LVs05 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:5]
					for lv in LVs05:
						s4 = lv.start_value
						e4 = lv.end_value
						u4 = int(lv.unit)

						if aLPG >= e4:
							v4 = invalue(u4*(e4-e3))
							t4 = tax_v(v4)
							r4 = e4-e3

						elif aLPG < s4:
							v4 = int(0)
						else:
							v4 = invalue(u4*(aLPG-e3))
							t4 = tax_v(v4)
							r4 = aLPG - e3

					LVs06 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:6]
					for lv in LVs06:
						s5 = lv.start_value
						e5 = lv.end_value
						u5 = int(lv.unit)

						if aLPG >= e5:
							v5 = invalue(u5*(e5-e4))
							t5 = tax_v(v5)
							r5 = e5-e4

						elif aLPG < s5:
							v5 = int(0)
						else:
							v5 = invalue(u5*(aLPG-e4))
							t5 = tax_v(v5)
							r5 = aLPG - e4

					LVs07 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:7]
					for lv in LVs07:
						s6 = lv.start_value
						e6 = lv.end_value
						u6 = int(lv.unit)

						if aLPG >= e6:
							v6 = invalue(u6*(e6-e5))
							t6 = tax_v(v6)
							r6 = e6-e5

						elif aLPG < s6:
							v6 = int(0)
						else:
							v6 = invalue(u6*(aLPG-e5))
							t6 = tax_v(v6)
							r6 = aLPG - e5

					context['s_code'] = s_code
					context['cLPG'] = cLPG
					context['bLPG'] = bLPG
					context['taxLPG'] = taxLPG

					context['s0'] = s0
					context['e0'] = e0
					context['u0'] = u0
					context['v0'] = v0
					context['r0'] = r0
					context['t0'] = t0

					context['s1'] = s1
					context['e1'] = e1
					context['u1'] = u1
					context['v1'] = v1
					context['r1'] = r1
					context['t1'] = t1

					context['s2'] = s2
					context['e2'] = e2
					context['u2'] = u2
					context['v2'] = v2
					context['r2'] = r2
					context['t2'] = t2

					context['s3'] = s3
					context['e3'] = e3
					context['u3'] = u3
					context['v3'] = v3
					context['r3'] = r3
					context['t3'] = t3

					context['s4'] = s4
					context['e4'] = e4
					context['u4'] = u4
					context['v4'] = v4
					context['r4'] = r4
					context['t4'] = t4

					context['s5'] = s5
					context['e5'] = e5
					context['u5'] = u5
					context['v5'] = v5
					context['r5'] = r5
					context['t5'] = t5

					context['s6'] = s6
					context['e6'] = e6
					context['u6'] = u6
					context['v6'] = v6
					context['r6'] = r6
					context['t6'] = t6


					context['base_product'] = "基本料金"
					context['product'] = "ガス使用料"
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
