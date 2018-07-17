#//+------------------------------------------------------------------+
#//|                 VerysVeryInc.Python3.Django.TemplateTags.Math.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Py3.Dj.TempTags.Filter.py - Ver.3.10.10 Update:2018.07.04" |
#//+------------------------------------------------------------------+
#//|                                    rinne_grid (id:rinne_grid2_1) |
#//|                 http://www.rinsymbol.net/entry/2015/04/30/095552 |
#//+------------------------------------------------------------------+
#//|               id:domodomodomo http://nihaoshijie.hatenadiary.jp/ |
#//|        http://nihaoshijie.hatenadiary.jp/entry/2017/12/19/013413 |
#//+------------------------------------------------------------------+
#//|                                                            @Usek |
#//|                https://qiita.com/Usek/items/53527feba2adcb386aa8 |
#//+------------------------------------------------------------------+
#//|                                                       @yoheiMune |
#//|                       https://www.yoheim.net/blog.php?q=20160409 |
#//+------------------------------------------------------------------+
#//|                                                    @beatdown0514 |
#//|        https://qiita.com/beatdown0514/items/361d6c213c2a1f2f5767 |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
# from django.template.defaultfilters import register

from django import template
register = template.Library()

import math
from Finance.models import Value_Test10, Value_Test30, Bank_Test20, Invoice_Test20
# from django.http import QueryDict
from django.utils import dateformat
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
# import time

jtax = 0.08
ndigits = 0


### New ###
# GC_SC
@register.filter("gc_sc")
def gc_sc(gc, sc):
	return gc, sc


# Change_Int
@register.filter("change_int")
def change_int(value):
    return int(value)


# Red_Value
@register.filter("red_value")
def red_value(value, rv):
	if(rv == 8):
		values = -(value)
	else:
		values = value
	return int(values)


# Division
@register.filter("divistion")
def division(value, args):
	return value / args


# Get_Unit
@register.filter("get_unit")
def get_unit(gcsc, md):
	gc, sc = gcsc

	try:
		if Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md)

			for v in s_values:
				sv = v.value
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md)

			for v in s_values:
				sv = v.value01
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md)

			for v in s_values:
				sv = v.value02
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md)

			for v in s_values:
				sv = v.value03
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md)

			for v in s_values:
				sv = v.value04
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md)

			for v in s_values:
				sv = v.value05
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md)

			for v in s_values:
				sv = v.value06
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md)

			for v in s_values:
				sv = v.value07
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md)

			for v in s_values:
				sv = v.value08
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md)

			for v in s_values:
				sv = v.value08
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md)

			for v in s_values:
				sv = v.value10
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md)

			for v in s_values:
				sv = v.value11
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md)

			for v in s_values:
				sv = v.value12
				return sv

		else:
			sv = 0
			return sv

	except Exception as e:
		print(e, 'get_unit : error occured')


# In_Tax : 内税
@register.filter("in_tax")
def in_tax(value):
	values = value - (value / (1+jtax))

	d_point = len(str(values).split('.')[1])
	ndigits = 0
	if ndigits >= d_point:
		return round(values, 0)
	c = (10 ** d_point) * 2

	return round((values * c + 1) / c, 0)


# Out_Tax : 外税
@register.filter("out_tax")
def out_tax(value):
	values = value * jtax

	d_point = len(str(values).split('.')[1])
	ndigits = 0
	if ndigits >= d_point:
		return round(values, 0)
	c = (10 ** d_point) * 2

	return round((values * c + 1) / c, 0)


# Cal_Tax
@register.filter("cal_tax")
def cal_tax(value):

	iTax = in_tax(value)	# 内税
	oTax = out_tax(value)	# 外税

	return iTax, oTax

# Check_Tax
@register.filter("chk_tax")
def chk_tax(gcsc, ivtax):
	gsm, amount = gcsc
	gs, md = gsm
	gc, sc = gs

	try:
		sv = get_unit(gs, md)
		cv = sv * (amount/100)

		# iTax:内税 | oTax:外税
		iTax, oTax = cal_tax(cv)

		# ivtax : True
		if ivtax != 0:
			# ハイオク.レギュラー.軽油 : 外税
			if sc == "10000" or sc == "10100" or sc == "10200":
				if ivtax == oTax:
					cTax = 0
				else:
					cTax = 10

			# 灯油.油外 : 内税
			else:
				if ivtax == iTax:
					# cTax = ""	# AWS単価 = POS単価
					cTax = 1
				else:
					# cTax = "*"	# AWS単価 ≠ POS単価
					cTax = 11

		# iv.tax : False
		else:
			# ハイオク.レギュラー.軽油 : 外税
			if sc == "10000" or sc == "10100" or sc == "10200":
				cTax = oTax

			# 灯油.油外 : 内税
			else:
				cTax = iTax

			# cTax = 20

		return cTax

		''' (Def)
		if ivtax == iTax:
			cTax = "iTax.OK"
		elif ivtax == oTax:
			cTax = "oTax.OK"
		else:
			cTax = "NG"

		return cTax
		'''

	except ZeroDivisionError as e:
		return print(e, 'chk_tax : ZeroDivisionError')



# Check_Unit
@register.filter("chk_unit")
def chk_unit(gcsc, ivunit):
	gsm, amount = gcsc
	gs, md = gsm

	try:
		sv = get_unit(gs, md)

		if ivunit == sv:
			cUnit = 1

		else:
			cUnit = 0

		return cUnit


	except ZeroDivisionError as e:
		return print(e, 'chk_unit : ZeroDivisionError')




# Cal_Value
'''
@register.filter("cal_value")
def cal_value(gcsc, amount):
	gs, md = gcsc
	sv = get_unit(gs, md)

	try:
		cv = sv * (amount/100)

		iTax, oTax = cal_tax(cv)

		return oTax

	except ZeroDivisionError as e:
		return print(e, 'check_unit_total : ZeroDivisionError')
'''




### OLD ###
@register.filter("merge_day")
def merge_day(gc, dlms):

	# dls = len(dlms)
	lastmonths = Invoice_Test20.objects.filter(g_code__uid=gc).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

	dlmm = lastmonths.dates('m_datetime', 'month', order='ASC')
	for dl in dlmm:
		dls = dl

	return dls


@register.filter("day_list")
def day_list(dls_daylist):

	dls, day_list = dls_daylist

	# print(day_list)
	# print(day_list[0])


	return day_list



@register.filter("check_day")
def check_day(gc, dlm):

	dd = dlm.day

	day_list = list()

	try:
		if Bank_Test20.objects.all().filter(uid=gc):
			d_values = Bank_Test20.objects.all().filter(uid=gc)

			for d in d_values:
				dv = d.check_day

				if dv != 0:
					if dd >= dv:	# 31 >= 25
						dls = (dlm + relativedelta(months=1)) - timedelta(days=dd-1) + timedelta(days=dv)
						# day_list = day_list + datetime.strftime(dls, '%Y-%m-%d')
						# day_list = datetime.strftime(dls, '%Y-%m-%d')

					elif dd < dv:	# 16 < 25
						dls = dlm - timedelta(days=dd) + timedelta(days=dv)
						# day_list = day_list + datetime.strftime(dls, '%Y-%m-%d')
						# day_list = datetime.strftime(dls, '%Y-%m-%d')
					else:
						dls = dlm + relativedelta(months=1) - timedelta(days=dd)
						# day_list = day_list + datetime.strptime(str(dls), '%Y-%m-%d')
						# day_list = datetime.strftime(dls, '%Y-%m-%d')

				else:
					# dls = dlm - timedelta(days=dd) + relativedelta(months=1)
					dls = dlm + relativedelta(months=1) - timedelta(days=dd)
					# day_list += datetime.strftime(dls, '%Y-%m-%d')
					day_list += datetime.strftime(dls, '%Y-%m-%d').split("''")
					# days = day_list.append( datetime.strftime(dls, "%Y-%m-%d") )
					# days = day_list.append( dls )


				# return dls

				return dls, day_list
				# return dls, days

				''' (OK)
				if dv != 0:
					# dls = dlm - relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
					# dls = dlm - relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
					dls = dlm

				else:
					dls = dlm - timedelta(days=1)

				return dls
				# return dv
				'''
		else:
			return 0, 0

	except Exception as e:
		print(e, 'check_day : error occured')

    # return dlm

'''
@register.filter("md_gc")
def md_gc(md, gc):

	mdt = datetime.strptime(md, '%Y-%m-%d')

	return md, gc

@register.filter("mdgc_sc")
def mdgc_sc(mdgc, sc):

	md, gc = mdgc

	return sc
'''


@register.filter("gc_sc")
def gc_sc(gc, sc):

	return gc, sc


@register.filter("sc_value")
def sc_value(gcsc, md):

	gc, sc = gcsc

	# d = md.replace('"','')
	# mdt = datetime.strptime(d, '%Y-%m-%d %H:%M:%S')

	# mdt = datetime.strptime(md, '%Y-%m-%d %H:%M:%S.%f')
	# mdt = mdt.replace(microsecond=0)

	# mdt = datetime.datetime.strptime(md, '%Y-%m-%d %H:%M:%S')

	try:
		if Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md)

			for v in s_values:
				sv = v.value
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md)

			for v in s_values:
				sv = v.value01
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md)

			for v in s_values:
				sv = v.value02
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md)

			for v in s_values:
				sv = v.value03
				return sv

		else:
			sv = 0
			return sv


	except Exception as e:
		print(e, 'sc_value : error occured')

	# return md


@register.filter("kc_value")
def kc_value(gcsc, md):

	gc, sc = gcsc

	try:
		if Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md)

			for v in s_values:
				sv = v.value - 32.1
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md)

			for v in s_values:
				sv = v.value01 - 32.1
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md)

			for v in s_values:
				sv = v.value02 - 32.1
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md)

			for v in s_values:
				sv = v.value03 - 32.1
				return sv

		else:
			sv = 0
			return sv

	except Exception as e:
		print(e, 'kc_value : error occured')


	# return sc



@register.filter("s_code_value")
def s_code_value(gc, sc):

	# (Ver.3.7.8.OK) s_values = Value_Test10.objects.all().filter(uid__endswith=gc, s_code=sc)
	s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc)

	for v in s_values:
		sv = v.value

		return sv



@register.filter("keiyu_code_value")
def keiyu_code_value(gc, sc):

	# (Ver.3.7.8.OK) s_values = Value_Test10.objects.all().filter(uid__endswith=gc, s_code=sc)
	s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc)

	for v in s_values:
		sv = v.value - 32.1

		return sv



@register.filter("check_unit01")
def check_unit01(gcsc, md):

	# value, tax = gcsc
	vtgcsc, amount = gcsc
	vtgc, sc = vtgcsc
	vt, gc = vtgc
	value, tax = vt

	try:
		uc = (value+tax) / (amount/100)

		if Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md)

			for v in s_values:
				sv = v.value

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md)

			for v in s_values:
				sv = v.value01
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md)

			for v in s_values:
				sv = v.value02
				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md)

			for v in s_values:
				sv = v.value03

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md)

			for v in s_values:
				sv = v.value04

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md)

			for v in s_values:
				sv = v.value05

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md)

			for v in s_values:
				sv = v.value06

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md)

			for v in s_values:
				sv = v.value07

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md)

			for v in s_values:
				sv = v.value08

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date09__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date09__lte=md)

			for v in s_values:
				sv = v.value09

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md)

			for v in s_values:
				sv = v.value10

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md)

			for v in s_values:
				sv = v.value11

				return sv

		elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md):
			s_values = Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md)

			for v in s_values:
				sv = v.value12

				return sv

		else:
			sv = uc
			return sv

	except Exception as e:
		print(e, 'check_unit01 : error occured')


	# return md


@register.filter("check_unit")
def check_unit(gcsc, amount):
# def check_unit(value, amount):

	value, tax = gcsc

	try:
		uc = (value+tax) / (amount/100)

		if uc.is_integer():
			return uc
		else:
			values = (value*1.00) / (amount/100)
			return values

		# values = (value * 1.08 ) / ( amount / 100 )
		# (OK) values = (value * 1.00 ) / ( amount / 100 )
		# (OK) return values
	except ZeroDivisionError as e:
		return print(e, 'check_unit : ZeroDivisionError')

	# return values

	'''
	if unit == 0:
		units = amount
	else:
		units = unit

	return units
	'''

@register.filter("check_tax")
def check_tax(gcsc, amount):

	vgc, sc = gcsc
	value, gc = vgc

	return sc


@register.filter("check_tax_code")
def check_tax_code(gcsc, amount):

	value, tax = gcsc

	try:
		uc = (value+tax) / (amount/100)

		if uc.is_integer():
			if tax > 0:
				return str("")
			else:
				return str("内")
		else:
			# return str("uchi")
			return str("内")

	except ZeroDivisionError as e:
		return print(e, 'check_tax_code : ZeroDivisionError')


@register.filter("check_unit_tax")
def check_unit_tax(gcsc, amount):

	value, tax = gcsc

	try:
		uc = (value+tax) / (amount/100)

		if uc.is_integer():
			values = (value+tax) - ((value+tax)/(1+jtax))
			d_point = len(str(values).split('.')[1])
			if ndigits >= d_point:
				return round(values, 0)
			c = (10 ** d_point) * 2
			return round((values * c + 1) / c, 0)

		else:
			values = value - (value/(1+jtax))
			d_point = len(str(values).split('.')[1])
			if ndigits >= d_point:
				return round(values, 0)
			c = (10 ** d_point) * 2
			return round((values * c + 1) / c, 0)

	except ZeroDivisionError as e:
		return print(e, 'check_unit_tax : ZeroDivisionError')



@register.filter("check_unit_total")
def check_unit_total(gcsc, amount):

	value, tax = gcsc

	try:
		uc = (value+tax) / (amount/100)

		if uc.is_integer():
			return value + tax
		else:
			return value

	except ZeroDivisionError as e:
		return print(e, 'check_unit_total : ZeroDivisionError')





@register.filter("notax")
def notax(value, args):
	values = value * (args / 100)

	d_point = len(str(values).split('.')[1])
	ndigits = 0

	if ndigits >= d_point:
		return round(values, 0)

	c = (10 ** d_point) * 2

	return round((values * c + 1) / c, 0)

	# values = math.floor(value * args / 100)
	# values = -(-value * args / 100)
	# values = round(value * (args / 100), 0)
	# return int(values)

@register.filter("intax")
def intax(value, args):
	if args != 0:
		values = args + value
		return values

	else:
		# values = -(-value * 0.08) + value
		# values = round(value * 0.08, 0) + value
		values = value * 0.08 + value

		d_point = len(str(values).split('.')[1])
		ndigits = 0

		if ndigits >= d_point:
			return round(values, 0)

		c = (10 ** d_point) * 2

		return round((values * c + 1) / c, 0)


	# return int(values)

	# values = math.floor(value * args / 100)
	# values = -(-value * args / 100)
	# return int(values)


@register.filter("s_tax")
def s_tax(sc, tax_value):
# def s_tax(sc):

	# if ハイオク.sc == "10000" or レギュラー.sc == "10100" or 軽油.sc == "10200" or sc == "10500":
	if sc == "10000" or sc == "10100" or sc == "10200":
		return str("")
	elif tax_value > 0:
		return str("")

	else:
		return str("内")

	# return sc

@register.filter("k_tax")
def k_tax(value, args):
	# values = math.floor(32.1 * args / 100)
	values = -(-32.1 * args / 100)
	return int(values)

@register.filter("c_tax")
def c_tax(value, args):

	if args != 0:
		values = args
		return values

	else:
		# values = -(-value * 0.08)
		# values = round(value * 0.08, 0)
		values = value * 0.08

		d_point = len(str(values).split('.')[1])
		ndigits = 0

		if ndigits >= d_point:
			return round(values, 0)

		c = (10 ** d_point) * 2

		return round((values * c + 1) / c, 0)

	# return int(values)



@register.filter("o_tax")
def o_tax(value, args):

	if args != 0:
		values = args
		return values

	else:
		# values = -(-value * 0.08)
		# values = round(value - (value / 1.08), 0)
		values = value - (value / 1.08)

		d_point = len(str(values).split('.')[1])
		ndigits = 0

		if ndigits >= d_point:
			return round(values, 0)

		c = (10 ** d_point) * 2

		return round((values * c + 1) / c, 0)

	# return int(values)





@register.filter("minus")
def minus(value, args):
	return value - args


@register.filter("multiplication")
def multiplication(value, args):
	return value * args
