#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Python3.Django.LPG.Views.py - Ver.3.11.26 Update:2018.06.07" |
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


class PDF_List(ListView):

	model = Name_Test20
	template_name = 'pdf_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['gid'] = self.kwargs.get('nid')

		dd_list = list()
		LPG_sTotal_list = list()
		sTotal_list = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')
			dlb = dlt + timedelta(days=1) - relativedelta(months=1)
			dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
			dld = dlb + timedelta(days=25)
			dldd = dld - timedelta(days=1)
			context['dlb'] = dlb
			context['dla'] = dla

			mLPG = datetime.strftime(dla, '%-m')
			dLPG = datetime.strftime(dld, '%-d')
			deLPG = datetime.strftime(dldd, '%-d')

			context['mLPG'] = mLPG
			context['dLPG'] = dLPG
			context['deLPG'] = deLPG

			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			ADs = Add_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### 住所 ###
			for ad in ADs:
				zipcode = ad.postal_code
				address = ad.address

			### 氏名 ###
			for na in NAs:
				names = na.name

			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG

			### LPG.料金コード ###
			for vl in VLs:
				cLPG = vl.lpg_code
				# context['cLPG'] = cLPG

				### LPG.ガス器具レンタル ###
				rLPG = vl.tax_code
				tax_rLPG = oTax_v(rLPG)
				notax_rLPG = rLPG - tax_rLPG

				context['rLPG'] = rLPG
				context['tax_rLPG'] = tax_rLPG

			### LPG.基本料金 ###
			LVs01 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:1]
			for lv in LVs01:
				bLPG = lv.base_value

			### LPG.検針実施日 ###
			try:
				for lm in LMs:
					if lm.m_datetime:
						date00 = lm.m_datetime
						dd00 = lm.m_datetime.day
						date00 = (date00-timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date00)

						### LPG.検針データ ###
						if dlt == date00:
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

					### Date:01 ###
					if lm.date01:
						date01 = lm.date01
						dd01 = lm.date01.day
						date01 = (date01-timedelta(days=dd01-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date01)

						### LPG.検針データ ###
						if dlt == date01:
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

					### Date:02 ###
					if lm.date02:
						date02 = lm.date02
						dd02 = lm.date02.day
						date02 = (date02-timedelta(days=dd02-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date02)

						### LPG.検針データ ###
						if dlt == date02:
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

					### Date:03 ###
					if lm.date03:
						date03 = lm.date03
						dd03 = lm.date03.day
						date03 = (date03-timedelta(days=dd03-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date03)

						### LPG.検針データ ###
						if dlt == date03:
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

					### Date:04 ###
					if lm.date04:
						date04 = lm.date04
						dd04 = lm.date04.day
						date04 = (date04-timedelta(days=dd04-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date04)

						### LPG.検針データ ###
						if dlt == date04:
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

					### Date:05 ###
					if lm.date05:
						date05 = lm.date05
						dd05 = lm.date05.day
						date05 = (date05-timedelta(days=dd05-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date05)

						### LPG.検針データ ###
						if dlt == date05:
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

					### Date:06 ###
					if lm.date06:
						date06 = lm.date06
						dd06 = lm.date06.day
						date06 = (date06-timedelta(days=dd06-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date06)

						### LPG.検針データ ###
						if dlt == date06:
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

					### Date:07 ###
					if lm.date07:
						date07 = lm.date07
						dd07 = lm.date07.day
						date07 = (date07-timedelta(days=dd07-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date07)

						### LPG.検針データ ###
						if dlt == date07:
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

					### Date:08 ###
					if lm.date08:
						date08 = lm.date08
						dd08 = lm.date08.day
						date08 = (date08-timedelta(days=dd08-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date08)

						### LPG.検針データ ###
						if dlt == date08:
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

					### Date:09 ###
					if lm.date09:
						date09 = lm.date09
						dd09 = lm.date09.day
						date09 = (date09-timedelta(days=dd09-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date09)

						### LPG.検針データ ###
						if dlt == date09:
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

					### Date:10 ###
					if lm.date10:
						date10 = lm.date10
						dd10 = lm.date10.day
						date10 = (date10-timedelta(days=dd10-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date10)

						### LPG.検針データ ###
						if dlt == date10:
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

					### Date:11 ###
					if lm.date11:
						date11 = lm.date11
						dd11 = lm.date11.day
						date11 = (date11-timedelta(days=dd11-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date11)

						### LPG.検針データ ###
						if dlt == date11:
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

					### Date:12 ###
					if lm.date12:
						date12 = lm.date12
						dd12 = lm.date12.day
						date12 = (date12-timedelta(days=dd12-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date12)

						### LPG.検針データ ###
						if dlt == date12:
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
				context['monLPG'] = monLPG
				context['dayLPG'] = dayLPG

				context['base_product'] = "基本料金"
				context['bLPG'] = bLPG
				context['product'] = "ガス使用量"
				context['aLPG'] = aLPG
				context['unit_product'] = "(ガス使用量 : 金額内訳)"
				context['rLPG_product'] = "(ガス器具)レンタル代"

				context['notax_values'] = sTotal + notax_rLPG
				context['tax_values'] = tax_sTotal + tax_rLPG

				context['LPG_values'] = lTotal + notax_rLPG
				context['LPG_tax_values'] = tax_lTotal + tax_rLPG

				total_values = sTotal + tax_sTotal + rLPG
				context['total_values'] = total_values

				context['all_total_values'] = total_values

			### LPG.検針実施日.Error ###
			except Exception as e:
				print(e, 'LPG/views.py_dds : error occured')


		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### 氏名 ###
			for na in NAs:
				names = na.name

			print(e, 'LPG/PDF/Views - PDF.DL.False : error occured')



		# context['Yuki'] = "祐希"

		context['zipcode'] = zipcode
		context['address'] = address
		context['names'] = names

		return context


	def render_to_response(self, context):
		html = get_template(self.template_name).render(self.get_context_data())
		result = io.BytesIO()

		pdf = pisa.pisaDocument(
			io.BytesIO(html.encode("UTF-8")),
			result,
			encoding='utf-8',
		)

		if not pdf.err:
			return HttpResponse(result.getvalue(), content_type='application/pdf')
		return None


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
		TJ_sTotal_List = list()
		sTotal_list = list()

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

			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			# LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'), m_datetime__lte=dlm)
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			LTs = LPG_ToJyu00.objects.all().filter(uid=self.kwargs.get('nid'))

			# context['lms'] = LMs

			### 氏名 ###
			for na in NAs:
				names = na.name

			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG

			### LPG.料金コード ###
			for vl in VLs:
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
						dd00 = lm.m_datetime.day
						date00 = (date00-timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date00)

						### LPG.検針データ ###
						if dlt == date00:
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

							'''
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

							context['s0'] = s0
							context['e0'] = e0
							context['u0'] = u0
							context['v0'] = v0
							context['r0'] = r0

							if v0 > 0:
								LPG_sTotal_list.append(v0)
							'''

							# r0 > 0
							if r0 > 0:
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)

								'''
								LVs02 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:2]
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

								context['s1'] = s1
								context['e1'] = e1
								context['u1'] = u1
								context['v1'] = v1
								context['r1'] = r1

								if v1 > 0:
									LPG_sTotal_list.append(v1)
								'''

							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)

								'''
								LVs03 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:3]
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

								context['s2'] = s2
								context['e2'] = e2
								context['u2'] = u2
								context['v2'] = v2
								context['r2'] = r2

								if v2 > 0:
									LPG_sTotal_list.append(v2)
								'''

							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)

								'''
								LVs04 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:4]
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

								context['s3'] = s3
								context['e3'] = e3
								context['u3'] = u3
								context['v3'] = v3
								context['r3'] = r3

								if v3 > 0:
									LPG_sTotal_list.append(v3)
								'''

							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)

								'''
								LVs05 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:5]
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
								context['s4'] = s4
								context['e4'] = e4
								context['u4'] = u4
								context['v4'] = v4
								context['r4'] = r4

								if v4 > 0:
									LPG_sTotal_list.append(v4)
								'''

							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)

								'''
								LVs06 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:6]
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

								context['s5'] = s5
								context['e5'] = e5
								context['u5'] = u5
								context['v5'] = v5
								context['r5'] = r5

								if v5 > 0:
									LPG_sTotal_list.append(v5)
								'''

							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

								'''
								LVs07 = LPG_Value00.objects.all().filter(uid=cLPG).order_by('start_value')[:7]
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

								context['s6'] = s6
								context['e6'] = e6
								context['u6'] = u6
								context['v6'] = v6
								context['r6'] = r6

								if v6 > 0:
									LPG_sTotal_list.append(v6)
								'''

						### LPG.小計 ###
						'''
						LPG_sTotal = sum(LPG_sTotal_list)
						context['LPG_sTotal'] = LPG_sTotal

						### 小計 ###
						sTotal_product = "[ 小計 ]"
						if LPG_sTotal > 0:
							sTotal = LPG_sTotal + bLPG
						else:
							sTotal = bLPG
						tax_sTotal = tax_v(sTotal)

						context['sTotal_product'] = sTotal_product
						context['sTotal'] = sTotal
						context['tax_sTotal'] = tax_sTotal
						'''

					if lm.date01:
						date01 = lm.date01
						dd01 = lm.date01.day
						date01 = (date01-timedelta(days=dd01-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date01)

						### LPG.検針データ ###
						if dlt == date01:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date02:
						date02 = lm.date02
						dd02 = lm.date02.day
						date02 = (date02-timedelta(days=dd02-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date02)

						### LPG.検針データ ###
						if dlt == date02:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date03:
						date03 = lm.date03
						dd03 = lm.date03.day
						date03 = (date03-timedelta(days=dd03-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date03)

						### LPG.検針データ ###
						if dlt == date03:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date04:
						date04 = lm.date04
						dd04 = lm.date04.day
						date04 = (date04-timedelta(days=dd04-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date04)

						### LPG.検針データ ###
						if dlt == date04:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date05:
						date05 = lm.date05
						dd05 = lm.date05.day
						date05 = (date05-timedelta(days=dd05-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date05)

						### LPG.検針データ ###
						if dlt == date05:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date06:
						date06 = lm.date06
						dd06 = lm.date06.day
						date06 = (date06-timedelta(days=dd06-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date06)

						### LPG.検針データ ###
						if dlt == date06:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date07:
						date07 = lm.date07
						dd07 = lm.date07.day
						date07 = (date07-timedelta(days=dd07-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date07)

						### LPG.検針データ ###
						if dlt == date07:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date08:
						date08 = lm.date08
						dd08 = lm.date08.day
						date08 = (date08-timedelta(days=dd08-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date08)

						### LPG.検針データ ###
						if dlt == date08:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date09:
						date09 = lm.date09
						dd09 = lm.date09.day
						date09 = (date09-timedelta(days=dd09-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date09)

						### LPG.検針データ ###
						if dlt == date09:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date10:
						date10 = lm.date10
						dd10 = lm.date10.day
						date10 = (date10-timedelta(days=dd10-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date10)

						### LPG.検針データ ###
						if dlt == date10:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date11:
						date11 = lm.date11
						dd11 = lm.date11.day
						date11 = (date11-timedelta(days=dd11-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date11)

						### LPG.検針データ ###
						if dlt == date11:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
								s6, e6, u6, v6, r6 = lvs07(aLPG, cLPG)

					if lm.date12:
						date12 = lm.date12
						dd12 = lm.date12.day
						date12 = (date12-timedelta(days=dd12-1)) + relativedelta(months=1) - timedelta(days=1)
						dd_list.append(date12)

						### LPG.検針データ ###
						if dlt == date12:
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
								# LPG.使用料金
								s1, e1, u1, v1, r1 = lvs02(aLPG, cLPG)
							# r1 > 0
							if r0 > 0 and r1 > 0:
								# LPG.使用料金
								s2, e2, u2, v2, r2 = lvs03(aLPG, cLPG)
							# r2 > 0
							if r0 > 0 and r1 > 0 and r2 > 0:
								# LPG.使用料金
								s3, e3, u3, v3, r3 = lvs04(aLPG, cLPG)
							# r3 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0:
								# LPG.使用料金
								s4, e4, u4, v4, r4 = lvs05(aLPG, cLPG)
							# r4 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0:
								# LPG.使用料金
								s5, e5, u5, v5, r5 = lvs06(aLPG, cLPG)
							# r5 > 0
							if r0 > 0 and r1 > 0 and r2 > 0 and r3 > 0 and r4 > 0 and r5 > 0:
								# LPG.使用料金
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
				context['cLPG'] = cLPG

				dds = sorted(set(dd_list), key=dd_list.index)
				context['dds'] = dds

				context['monLPG'] = monLPG
				context['dayLPG'] = dayLPG

				context['base_product'] = "基本料金"
				context['bLPG'] = bLPG
				context['product'] = "ガス使用量"
				context['aLPG'] = aLPG
				context['unit_product'] = "(ガス使用量 : 金額内訳)"
				context['rLPG_product'] = "(ガス器具) レンタル代"

				# context['notax_values'] = sTotal + notax_rLPG
				# context['tax_values'] = tax_sTotal + tax_rLPG

				context['LPG_values'] = lTotal + notax_rLPG
				context['LPG_tax_values'] = tax_lTotal + tax_rLPG

				# total_values = sTotal + tax_sTotal + rLPG
				# context['total_values'] = total_values

			### LPG.検針実施日.Error ###
			except Exception as e:
				print(e, 'LPG/views.py_dds : error occured')


			### LPG.灯油&A重油.取引日 ###
			try:
				for lt in LTs:
					if lt.date00:
						date00 = lt.date00
						dt00 = lt.date00.day
						date00 = (date00-timedelta(days=dt00-1)) + relativedelta(months=1) - timedelta(days=1)
						context['tlb'] = date00

						### LPG.灯油&A重油データ ###
						if dlt == date00:
							# 日付
							monToJyu = datetime.strftime(lt.date00, '%-m')
							dayToJyu = datetime.strftime(lt.date00, '%-d')

					if lt.date01:
						date01 = lt.date01
						dt01 = lt.date01.day
						date01 = (date01-timedelta(days=dt01-1)) + relativedelta(months=1) - timedelta(days=1)
						context['tlb'] = date01

						### LPG.灯油&A重油データ ###
						if dlt == date01:
							# 日付
							monToJyu = datetime.strftime(lt.date01, '%-m')
							dayToJyu = datetime.strftime(lt.date01, '%-d')

							# 商品コード
							ts_code = lt.s_code01

							if ts_code == "10500":
								ts_code_name = "灯油"
							if ts_code == "10600":
								ts_code_name = "A重油"

							# 供給量
							aTJ = lt.amount01

							# 単価
							uTJ = lt.unit01

							# 税込金額
							vTJ = lt.value01

							# 内税金額
							tax_TJ = oTax_v(vTJ)

							# 税別金額
							nontax_vTJ = vTJ - tax_TJ

				### LPG.Toyu&AJyuyu.Main ###
				context['monToJyu'] = monToJyu
				context['dayToJyu'] = dayToJyu

				context['ts_code'] = ts_code
				context['ts_code_name'] = ts_code_name

				context['aTJ'] = aTJ
				context['uTJ'] = uTJ
				context['vTJ'] = vTJ
				context['tax_TJ'] = tax_TJ
				context['nontax_vTJ'] = nontax_vTJ

				if ts_code != "10500":
					context['nonoil_values'] = nontax_vTJ

				context['notax_values'] = sTotal + notax_rLPG + nontax_vTJ
				context['tax_values'] = tax_sTotal + tax_rLPG + tax_TJ

				total_values = sTotal + tax_sTotal + rLPG + vTJ
				context['total_values'] = total_values

			### LPG.灯油&A重油.取引日.Error ###
			except Exception as e:
				print(e, 'LPG/views.py_dds.ToJyu : error occured')


		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter00.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			LTs = LPG_ToJyu00.objects.all().filter(uid=self.kwargs.get('nid'))

			### 検針実施日 ###
			try:
				for lm in LMs:
					if lm.m_datetime:
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

		### Paginator ###
		paginator = Paginator(LMs, 30)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1

		try:
			LMs = paginator.page(page)
		except(EmptyPage, InvalidPage):
			LMs = paginator.page(1)


		context['lms'] = LMs
		context['lts'] = LTs

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
