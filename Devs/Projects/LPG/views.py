#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Python3.Django.LPG.Views.py - Ver.3.11.35 Update:2018.06.10" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import HttpResponse

from django.views.generic import ListView
from .forms import NameForm

from Finance.models import Name_Test20, LPG_Meter10, Bank_Test20, Value_Test30, LPG_Value00, Add_Test20, LPG_ToJyu00
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
tDatetime = datetime(2018,3,31,23,59,59)

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

def tax_v_03(value, dlt, gid):
	if dlt <= tDatetime and gid == 120020:		# 岡山市可知保育園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 120028:	# 岡山市可知保育園 北
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 120030:	# 岡山市豊保育園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 120070:	# 岡山市立豊幼稚園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 120080:	# 岡山市太伯認定こども園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 120090:	# 岡山市金岡保育園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 130050:	# 岡山市西大寺保育園
		values = -(-value * jtax)
		return int(values)
	elif dlt <= tDatetime and gid == 130080:	# 公民館振興室（西大寺公民館 久保東分館）
		values = -(-value * jtax)
		return int(values)
	else:
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
	# 会社期末(決算月)
	if dm00 == company_line:
		dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
	# 締め日.25日
	elif dv == 25:
		if dd00 >= 25:
			dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) + timedelta(days=dv-1)
		else:
			dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=dv-1)
	# 締め日.25日以外
	elif dv != 25:
		if dv == dm00:
			dls = (date00 - timedelta(days=dd00-1)) + relativedelta(months=1) - timedelta(days=1)
		else:
			dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)
	# その他
	else:
		dls = (date00 - timedelta(days=dd00-1)) + timedelta(days=24)

	return dls


### PDF_List ###
class PDF_List(ListView):

	model = Name_Test20
	template_name = 'pdf_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		gid = self.kwargs.get('nid')
		context['gid'] = gid

		dd_list = list()
		LPG_sTotal_list = list()
		sTotal_list = list()

		aTJ_list = list()
		tTJ_list = list()
		ntax_vTJ_list = list()
		noil_ntax_vTJ_list = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')
			dm = dlt.month
			dd = dlt.day

			LMs = LPG_Meter10.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			LTs = LPG_ToJyu00.objects.all().filter(uid=self.kwargs.get('nid'))
			ADs = Add_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### LastDay : Check ###
			try:
				if BFs:
					d_values = BFs

					for d in d_values:
						dv = d.check_day

						if dd != 25:	# 締め日.25日以外
							dlb = (dlt - timedelta(days=dd-1)) - relativedelta(months=1) + timedelta(days=24)
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
							dld = dla
						elif dm == dv+1: # 締め日.25日以外.次月
							dlb = (dlt - timedelta(days=dd-1))
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
						elif dm == company_line:
							dlb = dlt - relativedelta(months=1) + timedelta(days=1)
							dla = (dlt - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(microseconds=1)
							dld = dla
						elif dm == company_line + 1:
							dlb = (dlt - timedelta(days=dd-1))
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
							dld = dlt + timedelta(days=1)
						else:
							dlb = dlt - relativedelta(months=1) + timedelta(days=1)
							dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
							dld = dlt + timedelta(days=1)

				context['dlb'] = dlb
				context['dla'] = dla

				mLPG = datetime.strftime(dla, '%-m')
				dLPG = datetime.strftime(dla, '%-d')
				deLPG = datetime.strftime(dld, '%-d')

				context['mLPG'] = mLPG
				context['dLPG'] = dLPG
				context['deLPG'] = deLPG

			### LastDay : Check.Error ###
			except Exception as e:
				print(e, 'LPG/views.dlb_dla : error occured')

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

				# 請求書フォーマット:BackImage.Setup
				if fLPG == 30:
					# fURL = "background-image: url('https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_30_02.png');"
					fURL = "https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_30_02.png"
				if fLPG == 300:
					fURL = "https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_300_02.png"
				context['fURL'] = fURL

			### LPG.料金コード : (2018-02-28.以前対応) ###
			for vl in VLs:
				if dlt < cDatetime and gid == 10805:	# ㈱東洋紡カンキョーテクノ 開発部
					cLPG = 908
				elif dlt < cDatetime and gid == 10806:	# ㈱東洋紡カンキョーテクノ 開発部No.2
					cLPG = 908
				elif dlt < cDatetime and gid == 130011:	# 吉原 栄
					cLPG = 915
				else:
					cLPG = vl.lpg_code

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
					else:
						sTotal = bLPG

					### LPG.税金 : (2018-03-31.以前.Tax小数点.切捨対応)
					tax_sTotal = tax_v_03(sTotal, dlt, gid)

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
				context['rLPG_product'] = "(ガス器具) レンタル代"

				context['notax_values'] = sTotal + notax_rLPG
				context['tax_values'] = tax_sTotal + tax_rLPG

				context['LPG_values'] = sTotal + notax_rLPG
				context['LPG_tax_values'] = tax_sTotal + tax_rLPG

				total_values = sTotal + tax_sTotal + rLPG
				context['total_values'] = total_values


			### LPG.検針実施日.Error ###
			except Exception as e:
				print(e, 'LPG/views.dds : error occured')


		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter10.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			ADs = Add_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			### 住所 ###
			for ad in ADs:
				zipcode = ad.postal_code
				address = ad.address

			### 氏名 ###
			for na in NAs:
				names = na.name

			print(e, 'LPG/PDF/Views - DL.False : error occured')



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


		### PDF.Main ###
		context['zipcode'] = zipcode
		context['address'] = address
		context['names'] = names

		context['lms'] = LMs

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

		aTJ_list = list()
		tTJ_list = list()
		ntax_vTJ_list = list()
		noil_ntax_vTJ_list = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')
			dm = dlt.month
			dd = dlt.day

			LMs = LPG_Meter10.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			LTs = LPG_ToJyu00.objects.all().filter(uid=self.kwargs.get('nid'))

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
				if dlt < cDatetime and gid == 10805:	# ㈱東洋紡カンキョーテクノ 開発部
					cLPG = 908
				elif dlt < cDatetime and gid == 10806:	# ㈱東洋紡カンキョーテクノ 開発部No.2
					cLPG = 908
				elif dlt < cDatetime and gid == 130011:	# 吉原 栄
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
						# lTotal = LPG_sTotal + bLPG
					else:
						sTotal = bLPG
						# lTotal = bLPG

					### LPG.税金 : (2018-03-31.以前.Tax小数点.切捨対応)
					tax_sTotal = tax_v_03(sTotal, dlt, gid)
					# tax_sTotal = tax_v(sTotal)
					# tax_lTotal = tax_v(lTotal)

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

				# context['LPG_values'] = lTotal + notax_rLPG
				# context['LPG_tax_values'] = tax_lTotal + tax_rLPG

				context['LPG_values'] = sTotal + notax_rLPG
				context['LPG_tax_values'] = tax_sTotal + tax_rLPG

				# context['notax_values'] = sTotal + notax_rLPG
				# context['tax_values'] = tax_sTotal + tax_rLPG

				# total_values = sTotal + tax_sTotal + rLPG
				# context['total_values'] = total_values

			### LPG.検針実施日.Error ###
			except Exception as e:
				print(e, 'LPG/views.dds : error occured')


			### LPG.灯油 & A重油.取引日 ###
			try:
				for lt in LTs:
					if lt.date00:
						date00 = lt.date00
						if dlb <= date00 and date00 <= dla:
							context['dTJ00'] = date00

							sTJ00 = lt.s_code00
							context['sTJ00'] = sTJ00

							if sTJ00 == "10500":
								s_code_name = "灯油"
							if sTJ00 == "10600":
								s_code_name = "A重油"
							context['sTJ_name00'] = s_code_name

							aTJ00 = lt.amount00
							context['aTJ00'] = aTJ00

							uTJ00 = lt.unit00
							context['uTJ00'] = uTJ00

							vTJ00 = lt.value00
							context['vTJ00'] = vTJ00

							tTJ00 = oTax_v(lt.value00)
							context['tTJ00'] = tTJ00
							tTJ_list.append(tTJ00)

							ntax_vTJ00 = vTJ00 - tTJ00

							if sTJ00 == "10500":
								aTJ_list.append(aTJ00)
								ntax_vTJ_list.append(ntax_vTJ00)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ00)

					if lt.date01:
						date01 = lt.date01
						if dlb <= date01 and date01 <= dla:
							context['dTJ01'] = date01

							sTJ01 = lt.s_code01
							context['sTJ01'] = sTJ01

							if sTJ01 == "10500":
								s_code_name = "灯油"
							if sTJ01 == "10600":
								s_code_name = "A重油"
							context['sTJ_name01'] = s_code_name

							aTJ01 = lt.amount01
							context['aTJ01'] = aTJ01

							uTJ01 = lt.unit01
							context['uTJ01'] = uTJ01

							vTJ01 = lt.value01
							context['vTJ01'] = vTJ01

							tTJ01 = oTax_v(lt.value01)
							context['tTJ01'] = tTJ01
							tTJ_list.append(tTJ01)

							ntax_vTJ01 = vTJ01 - tTJ01

							if sTJ01 == "10500":
								aTJ_list.append(aTJ01)
								ntax_vTJ_list.append(ntax_vTJ01)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ01)

					if lt.date02:
						date02 = lt.date02
						if dlb <= date02 and date02 <= dla:
							context['dTJ02'] = date02

							sTJ02 = lt.s_code02
							context['sTJ02'] = sTJ02

							if sTJ02 == "10500":
								s_code_name = "灯油"
							if sTJ02 == "10600":
								s_code_name = "A重油"
							context['sTJ_name02'] = s_code_name

							aTJ02 = lt.amount02
							context['aTJ02'] = aTJ02

							uTJ02 = lt.unit02
							context['uTJ02'] = uTJ02

							vTJ02 = lt.value02
							context['vTJ02'] = vTJ02

							tTJ02 = oTax_v(lt.value02)
							context['tTJ02'] = tTJ02
							tTJ_list.append(tTJ02)

							ntax_vTJ02 = vTJ02 - tTJ02

							if sTJ02 == "10500":
								aTJ_list.append(aTJ02)
								ntax_vTJ_list.append(ntax_vTJ02)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ02)

					if lt.date03:
						date03 = lt.date03
						if dlb <= date03 and date03 <= dla:
							context['dTJ03'] = date03

							sTJ03 = lt.s_code03
							context['sTJ03'] = sTJ03

							if sTJ03 == "10500":
								s_code_name = "灯油"
							if sTJ03 == "10600":
								s_code_name = "A重油"
							context['sTJ_name03'] = s_code_name

							aTJ03 = lt.amount03
							context['aTJ03'] = aTJ03

							uTJ03 = lt.unit03
							context['uTJ03'] = uTJ03

							vTJ03 = lt.value03
							context['vTJ03'] = vTJ03

							tTJ03 = oTax_v(lt.value03)
							context['tTJ03'] = tTJ03
							tTJ_list.append(tTJ03)

							ntax_vTJ03 = vTJ03 - tTJ03

							if sTJ03 == "10500":
								aTJ_list.append(aTJ03)
								ntax_vTJ_list.append(ntax_vTJ03)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ03)

					if lt.date04:
						date04 = lt.date04
						if dlb <= date04 and date04 <= dla:
							context['dTJ04'] = date04

							sTJ04 = lt.s_code04
							context['sTJ04'] = sTJ04

							if sTJ04 == "10500":
								s_code_name = "灯油"
							if sTJ04 == "10600":
								s_code_name = "A重油"
							context['sTJ_name04'] = s_code_name

							aTJ04 = lt.amount04
							context['aTJ04'] = aTJ04

							uTJ04 = lt.unit04
							context['uTJ04'] = uTJ04

							vTJ04 = lt.value04
							context['vTJ04'] = vTJ04

							tTJ04 = oTax_v(lt.value04)
							context['tTJ04'] = tTJ04
							tTJ_list.append(tTJ04)

							ntax_vTJ04 = vTJ04 - tTJ04

							if sTJ04 == "10500":
								aTJ_list.append(aTJ04)
								ntax_vTJ_list.append(ntax_vTJ04)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ04)

					if lt.date05:
						date05 = lt.date05
						if dlb <= date05 and date05 <= dla:
							context['dTJ05'] = date05

							sTJ05 = lt.s_code05
							context['sTJ05'] = sTJ05

							if sTJ05 == "10500":
								s_code_name = "灯油"
							if sTJ05 == "10600":
								s_code_name = "A重油"
							context['sTJ_name05'] = s_code_name

							aTJ05 = lt.amount05
							context['aTJ05'] = aTJ05

							uTJ05 = lt.unit05
							context['uTJ05'] = uTJ05

							vTJ05 = lt.value05
							context['vTJ05'] = vTJ05

							tTJ05 = oTax_v(lt.value05)
							context['tTJ05'] = tTJ05
							tTJ_list.append(tTJ05)

							ntax_vTJ05 = vTJ05 - tTJ05

							if sTJ05 == "10500":
								aTJ_list.append(aTJ05)
								ntax_vTJ_list.append(ntax_vTJ05)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ05)

					if lt.date06:
						date06 = lt.date06
						if dlb <= date06 and date06 <= dla:
							context['dTJ06'] = date06

							sTJ06 = lt.s_code06
							context['sTJ06'] = sTJ06

							if sTJ06 == "10500":
								s_code_name = "灯油"
							if sTJ06 == "10600":
								s_code_name = "A重油"
							context['sTJ_name06'] = s_code_name

							aTJ06 = lt.amount06
							context['aTJ06'] = aTJ06

							uTJ06 = lt.unit06
							context['uTJ06'] = uTJ06

							vTJ06 = lt.value06
							context['vTJ06'] = vTJ06

							tTJ06 = oTax_v(lt.value06)
							context['tTJ06'] = tTJ06
							tTJ_list.append(tTJ06)

							ntax_vTJ06 = vTJ06 - tTJ06

							if sTJ06 == "10500":
								aTJ_list.append(aTJ06)
								ntax_vTJ_list.append(ntax_vTJ06)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ06)

					if lt.date07:
						date07 = lt.date07
						if dlb <= date07 and date07 <= dla:
							context['dTJ07'] = date07

							sTJ07 = lt.s_code07
							context['sTJ07'] = sTJ07

							if sTJ07 == "10500":
								s_code_name = "灯油"
							if sTJ07 == "10600":
								s_code_name = "A重油"
							context['sTJ_name07'] = s_code_name

							aTJ07 = lt.amount07
							context['aTJ07'] = aTJ07

							uTJ07 = lt.unit07
							context['uTJ07'] = uTJ07

							vTJ07 = lt.value07
							context['vTJ07'] = vTJ07

							tTJ07 = oTax_v(lt.value07)
							context['tTJ07'] = tTJ07
							tTJ_list.append(tTJ07)

							ntax_vTJ07 = vTJ07 - tTJ07

							if sTJ07 == "10500":
								aTJ_list.append(aTJ07)
								ntax_vTJ_list.append(ntax_vTJ07)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ07)

					if lt.date08:
						date08 = lt.date08
						if dlb <= date08 and date08 <= dla:
							context['dTJ08'] = date08

							sTJ08 = lt.s_code08
							context['sTJ08'] = sTJ08

							if sTJ08 == "10500":
								s_code_name = "灯油"
							if sTJ08 == "10600":
								s_code_name = "A重油"
							context['sTJ_name08'] = s_code_name

							aTJ08 = lt.amount08
							context['aTJ08'] = aTJ08

							uTJ08 = lt.unit08
							context['uTJ08'] = uTJ08

							vTJ08 = lt.value08
							context['vTJ08'] = vTJ08

							tTJ08 = oTax_v(lt.value08)
							context['tTJ08'] = tTJ08
							tTJ_list.append(tTJ08)

							ntax_vTJ08 = vTJ08 - tTJ08

							if sTJ08 == "10500":
								aTJ_list.append(aTJ08)
								ntax_vTJ_list.append(ntax_vTJ08)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ08)

					if lt.date09:
						date09 = lt.date09
						if dlb <= date09 and date09 <= dla:
							context['dTJ09'] = date09

							sTJ09 = lt.s_code09
							context['sTJ09'] = sTJ09

							if sTJ09 == "10500":
								s_code_name = "灯油"
							if sTJ09 == "10600":
								s_code_name = "A重油"
							context['sTJ_name09'] = s_code_name

							aTJ09 = lt.amount09
							context['aTJ09'] = aTJ09

							uTJ09 = lt.unit09
							context['uTJ09'] = uTJ09

							vTJ09 = lt.value09
							context['vTJ09'] = vTJ09

							tTJ09 = oTax_v(lt.value09)
							context['tTJ09'] = tTJ09
							tTJ_list.append(tTJ09)

							ntax_vTJ09 = vTJ09 - tTJ09

							if sTJ09 == "10500":
								aTJ_list.append(aTJ09)
								ntax_vTJ_list.append(ntax_vTJ09)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ09)

					if lt.date10:
						date10 = lt.date10
						if dlb <= date10 and date10 <= dla:
							context['dTJ10'] = date10

							sTJ10 = lt.s_code10
							context['sTJ10'] = sTJ10

							if sTJ10 == "10500":
								s_code_name = "灯油"
							if sTJ10 == "10600":
								s_code_name = "A重油"
							context['sTJ_name10'] = s_code_name

							aTJ10 = lt.amount10
							context['aTJ10'] = aTJ10

							uTJ10 = lt.unit10
							context['uTJ10'] = uTJ10

							vTJ10 = lt.value10
							context['vTJ10'] = vTJ10

							tTJ10 = oTax_v(lt.value10)
							context['tTJ10'] = tTJ10
							tTJ_list.append(tTJ10)

							ntax_vTJ10 = vTJ10 - tTJ10

							if sTJ10 == "10500":
								aTJ_list.append(aTJ10)
								ntax_vTJ_list.append(ntax_vTJ10)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ10)

					if lt.date11:
						date11 = lt.date11
						if dlb <= date11 and date11 <= dla:
							context['dTJ11'] = date11

							sTJ11 = lt.s_code11
							context['sTJ11'] = sTJ11

							if sTJ11 == "10500":
								s_code_name = "灯油"
							if sTJ11 == "10600":
								s_code_name = "A重油"
							context['sTJ_name11'] = s_code_name

							aTJ11 = lt.amount11
							context['aTJ11'] = aTJ11

							uTJ11 = lt.unit11
							context['uTJ11'] = uTJ11

							vTJ11 = lt.value11
							context['vTJ11'] = vTJ11

							tTJ11 = oTax_v(lt.value11)
							context['tTJ11'] = tTJ11
							tTJ_list.append(tTJ11)

							ntax_vTJ11 = vTJ11 - tTJ11

							if sTJ11 == "10500":
								aTJ_list.append(aTJ11)
								ntax_vTJ_list.append(ntax_vTJ11)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ11)

					if lt.date12:
						date12 = lt.date12
						if dlb <= date12 and date12 <= dla:
							context['dTJ12'] = date12

							sTJ12 = lt.s_code12
							context['sTJ12'] = sTJ12

							if sTJ12 == "10500":
								s_code_name = "灯油"
							if sTJ12 == "10600":
								s_code_name = "A重油"
							context['sTJ_name12'] = s_code_name

							aTJ12 = lt.amount12
							context['aTJ12'] = aTJ12

							uTJ12 = lt.unit12
							context['uTJ12'] = uTJ12

							vTJ12 = lt.value12
							context['vTJ12'] = vTJ12

							tTJ12 = oTax_v(lt.value12)
							context['tTJ12'] = tTJ12
							tTJ_list.append(tTJ12)

							ntax_vTJ12 = vTJ12 - tTJ12

							if sTJ12 == "10500":
								aTJ_list.append(aTJ12)
								ntax_vTJ_list.append(ntax_vTJ12)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ12)

					if lt.date13:
						date13 = lt.date13
						if dlb <= date13 and date13 <= dla:
							context['dTJ13'] = date13

							sTJ13 = lt.s_code13
							context['sTJ13'] = sTJ13

							if sTJ13 == "10500":
								s_code_name = "灯油"
							if sTJ13 == "10600":
								s_code_name = "A重油"
							context['sTJ_name13'] = s_code_name

							aTJ13 = lt.amount13
							context['aTJ13'] = aTJ13

							uTJ13 = lt.unit13
							context['uTJ13'] = uTJ13

							vTJ13 = lt.value13
							context['vTJ13'] = vTJ13

							tTJ13 = oTax_v(lt.value13)
							context['tTJ13'] = tTJ13
							tTJ_list.append(tTJ13)

							ntax_vTJ13 = vTJ13 - tTJ13

							if sTJ13 == "10500":
								aTJ_list.append(aTJ13)
								ntax_vTJ_list.append(ntax_vTJ13)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ13)

					if lt.date14:
						date14 = lt.date14
						if dlb <= date14 and date14 <= dla:
							context['dTJ14'] = date14

							sTJ14 = lt.s_code14
							context['sTJ14'] = sTJ14

							if sTJ14 == "10500":
								s_code_name = "灯油"
							if sTJ14 == "10600":
								s_code_name = "A重油"
							context['sTJ_name14'] = s_code_name

							aTJ14 = lt.amount14
							context['aTJ14'] = aTJ14

							uTJ14 = lt.unit14
							context['uTJ14'] = uTJ14

							vTJ14 = lt.value14
							context['vTJ14'] = vTJ14

							tTJ14 = oTax_v(lt.value14)
							context['tTJ14'] = tTJ14
							tTJ_list.append(tTJ14)

							ntax_vTJ14 = vTJ14 - tTJ14

							if sTJ14 == "10500":
								aTJ_list.append(aTJ14)
								ntax_vTJ_list.append(ntax_vTJ14)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ14)

					if lt.date15:
						date15 = lt.date15
						if dlb <= date15 and date15 <= dla:
							context['dTJ15'] = date15

							sTJ15 = lt.s_code15
							context['sTJ15'] = sTJ15

							if sTJ15 == "10500":
								s_code_name = "灯油"
							if sTJ15 == "10600":
								s_code_name = "A重油"
							context['sTJ_name15'] = s_code_name

							aTJ15 = lt.amount15
							context['aTJ15'] = aTJ15

							uTJ15 = lt.unit15
							context['uTJ15'] = uTJ15

							vTJ15 = lt.value15
							context['vTJ15'] = vTJ15

							tTJ15 = oTax_v(lt.value15)
							context['tTJ15'] = tTJ15
							tTJ_list.append(tTJ15)

							ntax_vTJ15 = vTJ15 - tTJ15

							if sTJ15 == "10500":
								aTJ_list.append(aTJ15)
								ntax_vTJ_list.append(ntax_vTJ15)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ15)

					if lt.date16:
						date16 = lt.date16
						if dlb <= date16 and date16 <= dla:
							context['dTJ16'] = date16

							sTJ16 = lt.s_code16
							context['sTJ16'] = sTJ16

							if sTJ16 == "10500":
								s_code_name = "灯油"
							if sTJ16 == "10600":
								s_code_name = "A重油"
							context['sTJ_name16'] = s_code_name

							aTJ16 = lt.amount16
							context['aTJ16'] = aTJ16

							uTJ16 = lt.unit16
							context['uTJ16'] = uTJ16

							vTJ16 = lt.value16
							context['vTJ16'] = vTJ16

							tTJ16 = oTax_v(lt.value16)
							context['tTJ16'] = tTJ16
							tTJ_list.append(tTJ16)

							ntax_vTJ16 = vTJ16 - tTJ16

							if sTJ16 == "10500":
								aTJ_list.append(aTJ16)
								ntax_vTJ_list.append(ntax_vTJ16)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ16)

					if lt.date17:
						date17 = lt.date17
						if dlb <= date17 and date17 <= dla:
							context['dTJ17'] = date17

							sTJ17 = lt.s_code17
							context['sTJ17'] = sTJ17

							if sTJ17 == "10500":
								s_code_name = "灯油"
							if sTJ17 == "10600":
								s_code_name = "A重油"
							context['sTJ_name17'] = s_code_name

							aTJ17 = lt.amount17
							context['aTJ17'] = aTJ17

							uTJ17 = lt.unit17
							context['uTJ17'] = uTJ17

							vTJ17 = lt.value17
							context['vTJ17'] = vTJ17

							tTJ17 = oTax_v(lt.value17)
							context['tTJ17'] = tTJ17
							tTJ_list.append(tTJ17)

							ntax_vTJ17 = vTJ17 - tTJ17

							if sTJ17 == "10500":
								aTJ_list.append(aTJ17)
								ntax_vTJ_list.append(ntax_vTJ17)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ17)

					if lt.date18:
						date18 = lt.date18
						if dlb <= date18 and date18 <= dla:
							context['dTJ18'] = date18

							sTJ18 = lt.s_code18
							context['sTJ18'] = sTJ18

							if sTJ18 == "10500":
								s_code_name = "灯油"
							if sTJ18 == "10600":
								s_code_name = "A重油"
							context['sTJ_name18'] = s_code_name

							aTJ18 = lt.amount18
							context['aTJ18'] = aTJ18

							uTJ18 = lt.unit18
							context['uTJ18'] = uTJ18

							vTJ18 = lt.value18
							context['vTJ18'] = vTJ18

							tTJ18 = oTax_v(lt.value18)
							context['tTJ18'] = tTJ18
							tTJ_list.append(tTJ18)

							ntax_vTJ18 = vTJ18 - tTJ18

							if sTJ18 == "10500":
								aTJ_list.append(aTJ18)
								ntax_vTJ_list.append(ntax_vTJ18)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ18)

					if lt.date19:
						date19 = lt.date19
						if dlb <= date19 and date19 <= dla:
							context['dTJ19'] = date19

							sTJ19 = lt.s_code19
							context['sTJ19'] = sTJ19

							if sTJ19 == "10500":
								s_code_name = "灯油"
							if sTJ19 == "10600":
								s_code_name = "A重油"
							context['sTJ_name19'] = s_code_name

							aTJ19 = lt.amount19
							context['aTJ19'] = aTJ19

							uTJ19 = lt.unit19
							context['uTJ19'] = uTJ19

							vTJ19 = lt.value19
							context['vTJ19'] = vTJ19

							tTJ19 = oTax_v(lt.value19)
							context['tTJ19'] = tTJ19
							tTJ_list.append(tTJ19)

							ntax_vTJ19 = vTJ19 - tTJ19

							if sTJ19 == "10500":
								aTJ_list.append(aTJ19)
								ntax_vTJ_list.append(ntax_vTJ19)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ19)

					if lt.date20:
						date20 = lt.date20
						if dlb <= date20 and date20 <= dla:
							context['dTJ20'] = date20

							sTJ20 = lt.s_code20
							context['sTJ20'] = sTJ20

							if sTJ20 == "10500":
								s_code_name = "灯油"
							if sTJ20 == "10600":
								s_code_name = "A重油"
							context['sTJ_name20'] = s_code_name

							aTJ20 = lt.amount20
							context['aTJ20'] = aTJ20

							uTJ20 = lt.unit20
							context['uTJ20'] = uTJ20

							vTJ20 = lt.value20
							context['vTJ20'] = vTJ20

							tTJ20 = oTax_v(lt.value20)
							context['tTJ20'] = tTJ20
							tTJ_list.append(tTJ20)

							ntax_vTJ20 = vTJ20 - tTJ20

							if sTJ20 == "10500":
								aTJ_list.append(aTJ20)
								ntax_vTJ_list.append(ntax_vTJ20)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ20)

					if lt.date21:
						date21 = lt.date21
						if dlb <= date21 and date21 <= dla:
							context['dTJ21'] = date21

							sTJ21 = lt.s_code21
							context['sTJ21'] = sTJ21

							if sTJ21 == "10500":
								s_code_name = "灯油"
							if sTJ21 == "10600":
								s_code_name = "A重油"
							context['sTJ_name21'] = s_code_name

							aTJ21 = lt.amount21
							context['aTJ21'] = aTJ21

							uTJ21 = lt.unit21
							context['uTJ21'] = uTJ21

							vTJ21 = lt.value21
							context['vTJ21'] = vTJ21

							tTJ21 = oTax_v(lt.value21)
							context['tTJ21'] = tTJ21
							tTJ_list.append(tTJ21)

							ntax_vTJ21 = vTJ21 - tTJ21

							if sTJ21 == "10500":
								aTJ_list.append(aTJ21)
								ntax_vTJ_list.append(ntax_vTJ21)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ21)

					if lt.date22:
						date22 = lt.date22
						if dlb <= date22 and date22 <= dla:
							context['dTJ22'] = date22

							sTJ22 = lt.s_code22
							context['sTJ22'] = sTJ22

							if sTJ22 == "10500":
								s_code_name = "灯油"
							if sTJ22 == "10600":
								s_code_name = "A重油"
							context['sTJ_name22'] = s_code_name

							aTJ22 = lt.amount22
							context['aTJ22'] = aTJ22

							uTJ22 = lt.unit22
							context['uTJ22'] = uTJ22

							vTJ22 = lt.value22
							context['vTJ22'] = vTJ22

							tTJ22 = oTax_v(lt.value22)
							context['tTJ22'] = tTJ22
							tTJ_list.append(tTJ22)

							ntax_vTJ22 = vTJ22 - tTJ22

							if sTJ22 == "10500":
								aTJ_list.append(aTJ22)
								ntax_vTJ_list.append(ntax_vTJ22)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ22)

					if lt.date23:
						date23 = lt.date23
						if dlb <= date23 and date23 <= dla:
							context['dTJ23'] = date23

							sTJ23 = lt.s_code23
							context['sTJ23'] = sTJ23

							if sTJ23 == "10500":
								s_code_name = "灯油"
							if sTJ23 == "10600":
								s_code_name = "A重油"
							context['sTJ_name23'] = s_code_name

							aTJ23 = lt.amount23
							context['aTJ23'] = aTJ23

							uTJ23 = lt.unit23
							context['uTJ23'] = uTJ23

							vTJ23 = lt.value23
							context['vTJ23'] = vTJ23

							tTJ23 = oTax_v(lt.value23)
							context['tTJ23'] = tTJ23
							tTJ_list.append(tTJ23)

							ntax_vTJ23 = vTJ23 - tTJ23

							if sTJ23 == "10500":
								aTJ_list.append(aTJ23)
								ntax_vTJ_list.append(ntax_vTJ23)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ23)

					if lt.date24:
						date24 = lt.date24
						if dlb <= date24 and date24 <= dla:
							context['dTJ24'] = date24

							sTJ24 = lt.s_code24
							context['sTJ24'] = sTJ24

							if sTJ24 == "10500":
								s_code_name = "灯油"
							if sTJ24 == "10600":
								s_code_name = "A重油"
							context['sTJ_name24'] = s_code_name

							aTJ24 = lt.amount24
							context['aTJ24'] = aTJ24

							uTJ24 = lt.unit24
							context['uTJ24'] = uTJ24

							vTJ24 = lt.value24
							context['vTJ24'] = vTJ24

							tTJ24 = oTax_v(lt.value24)
							context['tTJ24'] = tTJ24
							tTJ_list.append(tTJ24)

							ntax_vTJ24 = vTJ24 - tTJ24

							if sTJ24 == "10500":
								aTJ_list.append(aTJ24)
								ntax_vTJ_list.append(ntax_vTJ24)
							else:
								noil_ntax_vTJ_list.append(ntax_vTJ24)

					### 灯油 & A重油 : 合計 ###
					aTJ = sum(aTJ_list)
					tTJ = sum(tTJ_list)
					ntax_vTJ = sum(ntax_vTJ_list)
					noil_ntax_vTJ = sum(noil_ntax_vTJ_list)

				### LPG.灯油 & A重油.Main ###
				context['notax_values'] = sTotal + notax_rLPG + (ntax_vTJ + noil_ntax_vTJ)
				context['tax_values'] = tax_sTotal + tax_rLPG + (tTJ)

				context['aTJ'] = aTJ
				context['ntax_vTJ'] = ntax_vTJ
				context['nonoil_values'] = noil_ntax_vTJ

				total_values = sTotal + tax_sTotal + rLPG + (ntax_vTJ + tTJ + noil_ntax_vTJ)
				context['total_values'] = total_values


			### LPG.灯油 & A重油.取引日.Error ###
			except Exception as e:
				print(e, 'LPG/views.Toyu.Jyuyu : error occured')


		### DL : False ###
		except Exception as e:
			LMs = LPG_Meter10.objects.all().filter(uid=self.kwargs.get('nid'))
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			LTs = LPG_ToJyu00.objects.all().filter(uid=self.kwargs.get('nid'))

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

		### ALL.Context ###
		context['names'] = names
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
