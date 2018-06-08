#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Python3.Django.LPG.Views.py - Ver.3.11.31 Update:2018.06.08" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import HttpResponse

from django.views.generic import ListView
from .forms import NameForm

from Finance.models import Name_Test20, LPG_Meter00, Bank_Test20, Value_Test30, LPG_Value00, Add_Test20, LPG_ToJyu00
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

# PDF #
import io
import os
from django.template.loader import get_template
from xhtml2pdf import pisa

jtax = 0.08
ndigits = 0
company_line = 7
cDatetime = datetime(2018,2,28,23,59,59)

def tax_v(value):
	values = value * jtax
	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		return int(round(values, 0))
	c = (10 ** d_point) * 2
	return int(round((values * c + 1) / c, 0))

def oTax_v(value):
	values = value - (value / (1+jtax))
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

def lvs01(aLPG, cLPG):
	LVs01 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:1]
	# LPG.使用料金
	for lv in LVs01:
		s0 = lv.start_value
		e0 = lv.end_value
		u0 = int(lv.unit)
		if aLPG >= e0:
			v0 = invalue(u0*(e0-s0))
			r0 = e0 - s0
		elif aLPG < s0:
			v0 = int(0)
			r0 = int(0)
		else:
			v0 = invalue(u0*(aLPG-s0))
			r0 = aLPG - s0
	return s0, e0, u0, v0, r0

def lvs02(aLPG, cLPG):
	s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

	LVs02 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:2]
	# LPG.使用料金
	for lv in LVs02:
		s1 = lv.start_value
		e1 = lv.end_value
		u1 = int(lv.unit)
		if aLPG >= e1:
			v1 = invalue(u1*(e1-e0))
			r1 = e1 - e0
		elif aLPG < s1:
			v1 = int(0)
			r1 = int(0)
		else:
			v1 = invalue(u1*(aLPG-e0))
			r1 = aLPG - e0
	return s1, e1, u1, v1, r1

def lvs03(aLPG, cLPG):
	s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)

	LVs03 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:3]
	# LPG.使用料金
	for lv in LVs03:
		s2 = lv.start_value
		e2 = lv.end_value
		u2 = int(lv.unit)
		if aLPG >= e2:
			v2 = invalue(u2*(e2-e1))
			r2 = e2-e1
		elif aLPG < s2:
			v2 = int(0)
			r2 = int(0)
		else:
			v2 = invalue(u2*(aLPG-e1))
			r2 = aLPG - e1
	return s2, e2, u2, v2, r2

def lvs04(aLPG, cLPG):
	s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)

	LVs04 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:4]
	# LPG.使用料金
	for lv in LVs04:
		s3 = lv.start_value
		e3 = lv.end_value
		u3 = int(lv.unit)
		if aLPG >= e3:
			v3 = invalue(u3*(e3-e2))
			r3 = e3-e2
		elif aLPG < s3:
			v3 = int(0)
			r3 = int(0)
		else:
			v3 = invalue(u3*(aLPG-e2))
			r3 = aLPG - e2
	return s3, e3, u3, v3, r3

def lvs05(aLPG, cLPG):
	s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)

	LVs05 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:5]
	# LPG.使用料金
	for lv in LVs05:
		s4 = lv.start_value
		e4 = lv.end_value
		u4 = int(lv.unit)
		if aLPG >= e4:
			v4 = invalue(u4*(e4-e3))
			r4 = e4-e3
		elif aLPG < s4:
			v4 = int(0)
			r4 = int(0)
		else:
			v4 = invalue(u4*(aLPG-e3))
			r4 = aLPG - e3
	return s4, e4, u4, v4, r4

def lvs06(aLPG, cLPG):
	s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)

	LVs06 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:6]
	# LPG.使用料金
	for lv in LVs06:
		s5 = lv.start_value
		e5 = lv.end_value
		u5 = int(lv.unit)
		if aLPG >= e5:
			v5 = invalue(u5*(e5-e4))
			r5 = e5-e4
		elif aLPG < s5:
			v5 = int(0)
			r5 = int(0)
		else:
			v5 = invalue(u5*(aLPG-e4))
			r5 = aLPG - e4
	return s5, e5, u5, v5, r5

def lvs07(aLPG, cLPG):
	s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)

	LVs07 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:7]
	# LPG.使用料金
	for lv in LVs07:
		s6 = lv.start_value
		e6 = lv.end_value
		u6 = int(lv.unit)
		if aLPG >= e6:
			v6 = invalue(u6*(e6-e5))
			r6 = e6-e5
		elif aLPG < s6:
			v6 = int(0)
			r6 = int(0)
		else:
			v6 = invalue(u6*(aLPG-e5))
			r6 = aLPG - e5
	return s6, e6, u6, v6, r6

def dds_dls(dv, date00, dm00, dd00):
	if dv == 25:
		if dd00 >= 25:
			dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) + timedelta(days=dv-1)
		else:
			dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=dv-1)
	if dv != 25:
		if dv == dm00:
			dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
		else:
			dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)
	else:
		dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)

	return dls





### PDF_List ###
class PDF_List(ListView):

	model = Name_Test20
	template_name = 'pdf_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		return context


### LPG_List ###
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
		gid = self.kwargs.get('nid')
		context['gid'] = gid

		dd_list = list()
		LPG_sTotal_list = list()
		sTotal_list = list()
		TJ_sTotal_List = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')
			dm = dlt.month
			dd = dlt.day

			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')

			### LastDay : Check ###
			try:
				if BFs:
					d_values = BFs

					for d in d_values:
						dv = d.check_day

						if dd != 25:
							dlb = (dlt - timedelta(days=dd-1)) - relativedelta(months=1) + timedelta(days=24)
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
						elif dm == dv+1:
							dlb = (dlt - timedelta(days=dd-1))
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
						elif dm == company_line:
							dlb = dlt - relativedelta(months=1) + timedelta(days=1)
							dla = (dlt - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(microseconds=1)
						elif dm == company_line + 1:
							dlb = (dlt - timedelta(days=dd-1))
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
						else:
							dlb = dlt - relativedelta(months=1) + timedelta(days=1)
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)

				context['dlb'] = dlb
				context['dla'] = dla


			### LastDay : Check.Error ###
			except Exception as e:
				print(e, 'LPG/views.dlb_dla : error occured')

			### 氏名 ###
			for na in NAs:
				names = na.name

			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG

			### LPG.料金コード : (2018-02-28.以前対応) ###
			for vl in VLs:
				if dlt < cDatetime and gid == 10805:
					cLPG = 908
				elif dlt < cDatetime and gid == 10806:
					cLPG = 908
				elif dlt < cDatetime and gid == 130011:
					cLPG = 915
				else:
					cLPG = vl.lpg_code
				# context['cLPG'] = cLPG

				### LPG.ガス器具レンタル ###
				rLPG = vl.tax_code
				tax_rLPG = oTax_v(rLPG)
				notax_rLPG = rLPG - tax_rLPG

				context['rLPG'] = rLPG
				context['tax_rLPG'] = tax_rLPG

			### PDF.リンク ###
			PDF_Link = "../PDF/%s/" % gid
			context['pLink'] = PDF_Link

			### LPG.基本料金 ###
			LVs01 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:1]
			for lv in LVs01:
				bLPG = lv.base_value

			### LPG.検針実施日 ###
			try:
				for lm in LMs:
					if lm.m_datetime:
						date00 = lm.m_datetime
						dm00 = lm.m_datetime.month
						dd00 = lm.m_datetime.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date00, dm00, dd00)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.m_datetime, '%-m')
							dayLPG = datetime.strftime(lm.m_datetime, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date01:
						date01 = lm.date01
						dm01 = lm.date01.month
						dd01 = lm.date01.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date01, dm01, dd01)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date01, '%-m')
							dayLPG = datetime.strftime(lm.date01, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount01

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date02:
						date02 = lm.date02
						dm02 = lm.date02.month
						dd02 = lm.date02.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date02, dm02, dd02)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date02, '%-m')
							dayLPG = datetime.strftime(lm.date02, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount02

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date03:
						date03 = lm.date03
						dm03 = lm.date03.month
						dd03 = lm.date03.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date03, dm03, dd03)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date03, '%-m')
							dayLPG = datetime.strftime(lm.date03, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount03

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date04:
						date04 = lm.date04
						dm04 = lm.date04.month
						dd04 = lm.date04.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date04, dm04, dd04)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date04, '%-m')
							dayLPG = datetime.strftime(lm.date04, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount04

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date05:
						date05 = lm.date05
						dm05 = lm.date05.month
						dd05 = lm.date05.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date05, dm05, dd05)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date05, '%-m')
							dayLPG = datetime.strftime(lm.date05, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount05

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date06:
						date06 = lm.date06
						dm06 = lm.date06.month
						dd06 = lm.date06.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date06, dm06, dd06)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date06, '%-m')
							dayLPG = datetime.strftime(lm.date06, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount06

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date07:
						date07 = lm.date07
						dm07 = lm.date07.month
						dd07 = lm.date07.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date07, dm07, dd07)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date07, '%-m')
							dayLPG = datetime.strftime(lm.date07, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount07

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date08:
						date08 = lm.date08
						dm08 = lm.date08.month
						dd08 = lm.date08.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date08, dm08, dd08)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date08, '%-m')
							dayLPG = datetime.strftime(lm.date08, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount08

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date09:
						date09 = lm.date09
						dm09 = lm.date09.month
						dd09 = lm.date09.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date09, dm09, dd09)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date09, '%-m')
							dayLPG = datetime.strftime(lm.date09, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount09

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date10:
						date10 = lm.date10
						dm10 = lm.date10.month
						dd10 = lm.date10.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date10, dm10, dd10)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date10, '%-m')
							dayLPG = datetime.strftime(lm.date10, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount10

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date11:
						date11 = lm.date11
						dm11 = lm.date11.month
						dd11 = lm.date11.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date11, dm11, dd11)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date11, '%-m')
							dayLPG = datetime.strftime(lm.date11, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount11

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date12:
						date12 = lm.date12
						dm12 = lm.date12.month
						dd12 = lm.date12.day
						for d in BFs:
							dv = d.check_day
							dls = dds_dls(dv, date12, dm12, dd12)
							dd_list.append(dls)

						### LPG.検針データ ###
						if dlt ==  dls:
							# 日付
							monLPG = datetime.strftime(lm.date12, '%-m')
							dayLPG = datetime.strftime(lm.date12, '%-d')

							# 商品コード
							s_code = lm.s_code
							context['s_code'] = s_code

							# LPG.使用量
							aLPG = lm.amount12

							# LPG.使用料金
							s0, e0, u0, v0, r0 = lvs01(aLPG, cLPG)

							# r0 > 0
							if r0 > 0:
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					### LPG.小計 ###
					# LVs01
					context['s0'] = s0
					context['e0'] = e0
					context['u0'] = u0
					context['v0'] = v0
					context['r0'] = r0
					if v0 > 0:
						LPG_sTotal_list.append(v0)

					# LVs02
					if r0 > 0:
						context['s1'] = s1
						context['e1'] = e1
						context['u1'] = u1
						context['v1'] = v1
						context['r1'] = r1
						if v1 > 0:
							LPG_sTotal_list.append(v1)

					# LVs03
					if r0 > 0 and r1 > 0:
						context['s2'] = s2
						context['e2'] = e2
						context['u2'] = u2
						context['v2'] = v2
						context['r2'] = r2
						if v2 > 0:
							LPG_sTotal_list.append(v2)

					# LVs04
					if r0 > 0 and r1 > 0 and r2 > 0:
						context['s3'] = s3
						context['e3'] = e3
						context['u3'] = u3
						context['v3'] = v3
						context['r3'] = r3
						if v3 > 0:
							LPG_sTotal_list.append(v3)

					# LVs05
					if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
						context['s4'] = s4
						context['e4'] = e4
						context['u4'] = u4
						context['v4'] = v4
						context['r4'] = r4
						if v4 > 0:
							LPG_sTotal_list.append(v4)

					# LVs06
					if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
						context['s5'] = s5
						context['e5'] = e5
						context['u5'] = u5
						context['v5'] = v5
						context['r5'] = r5
						if v5 > 0:
							LPG_sTotal_list.append(v5)

					# LVs07
					if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
						context['s6'] = s6
						context['e6'] = e6
						context['u6'] = u6
						context['v6'] = v6
						context['r6'] = r6
						if v6 > 0:
							LPG_sTotal_list.append(v6)

					LPG_sTotal = sum(LPG_sTotal_list)
					context['LPG_sTotal'] = LPG_sTotal


					### 小計 ###
					if LPG_sTotal > 0:
						sTotal = LPG_sTotal + bLPG
						lTotal = LPG_sTotal + bLPG
					else:
						sTotal = bLPG
						lTotal = bLPG
					tax_sTotal = tax_v(sTotal)
					tax_lTotal = tax_v(lTotal)

					sTotal_product = "[ 小計 ]"
					context['sTotal_product'] = sTotal_product
					context['sTotal'] = sTotal
					context['tax_sTotal'] = tax_sTotal


				### LPG.Main ###
				dds = sorted(set(dd_list), key=dd_list.index)
				context['dds'] = dds

				context['cLPG'] = cLPG

				context['monLPG'] = monLPG
				context['dayLPG'] = dayLPG

				context['base_product'] = "基本料金"
				context['bLPG'] = bLPG
				context['product'] = "ガス使用量"
				context['aLPG'] = aLPG
				context['unit_product'] = "(ガス使用量 : 金額内訳)"
				context['rLPG_product'] = "(ガス器具) レンタル代"

				context['LPG_values'] = lTotal + notax_rLPG
				context['LPG_tax_values'] = tax_lTotal + tax_rLPG

				context['notax_values'] = sTotal + notax_rLPG
				context['tax_values'] = tax_sTotal + tax_rLPG

				total_values = sTotal + tax_sTotal + rLPG
				context['total_values'] = total_values


			### LPG.検針実施日.Error ###
			except Exception as e:
				print(e, 'LPG/views.dds : error occured')

		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### LastDay : Check ###
			try:
				if Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid')):
					d_values = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

					for lm in LMs:
						if lm.m_datetime:
							date00 = lm.m_datetime
							dm00 = lm.m_datetime.month
							dd00 = lm.m_datetime.day

							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date00, dm00, dd00)

								'''
								if dv == 25:
									if dd00 >= 25:
										dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) + timedelta(days=dv-1)
									else:
										dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=dv-1)
								if dv != 25:
									if dv == dm00:
										dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
									else:
										dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)
								else:
									dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)
								'''

								dd_list.append(dls)

						if lm.date01:
							date01 = lm.date01
							dm01 = lm.date01.month
							dd01 = lm.date01.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date01, dm01, dd01)
								dd_list.append(dls)

						if lm.date02:
							date02 = lm.date02
							dm02 = lm.date02.month
							dd02 = lm.date02.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date02, dm02, dd02)
								dd_list.append(dls)

						if lm.date03:
							date03 = lm.date03
							dm03 = lm.date03.month
							dd03 = lm.date03.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date03, dm03, dd03)
								dd_list.append(dls)

						if lm.date04:
							date04 = lm.date04
							dm04 = lm.date04.month
							dd04 = lm.date04.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date04, dm04, dd04)
								dd_list.append(dls)

						if lm.date05:
							date05 = lm.date05
							dm05 = lm.date05.month
							dd05 = lm.date05.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date05, dm05, dd05)
								dd_list.append(dls)

						if lm.date06:
							date06 = lm.date06
							dm06 = lm.date06.month
							dd06 = lm.date06.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date06, dm06, dd06)
								dd_list.append(dls)

						if lm.date07:
							date07 = lm.date07
							dm07 = lm.date07.month
							dd07 = lm.date07.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date07, dm07, dd07)
								dd_list.append(dls)

						if lm.date08:
							date08 = lm.date08
							dm08 = lm.date08.month
							dd08 = lm.date08.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date08, dm08, dd08)
								dd_list.append(dls)

						if lm.date09:
							date09 = lm.date09
							dm09 = lm.date09.month
							dd09 = lm.date09.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date09, dm09, dd09)
								dd_list.append(dls)

						if lm.date10:
							date10 = lm.date10
							dm10 = lm.date10.month
							dd10 = lm.date10.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date10, dm10, dd10)
								dd_list.append(dls)

						if lm.date11:
							date11 = lm.date11
							dm11 = lm.date11.month
							dd11 = lm.date11.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date11, dm11, dd11)
								dd_list.append(dls)

						if lm.date12:
							date12 = lm.date12
							dm12 = lm.date12.month
							dd12 = lm.date12.day
							for d in d_values:
								dv = d.check_day
								dls = dds_dls(dv, date12, dm12, dd12)
								dd_list.append(dls)

					dds = sorted(set(dd_list), key=dd_list.index)
					context['dds'] = dds

			### LastDay : Check.Error ###
			except Exception as e:
				print(e, 'LPG/views.py_dds : error occured')

			### 氏名 ###
			for na in NAs:
				names = na.name

			print(e, 'LPG/Views - DL.False : error occured')

		### ALL.Context ###
		context['names'] = names
		context['lms'] = LMs

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
