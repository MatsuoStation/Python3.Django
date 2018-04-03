#//+------------------------------------------------------------------+
#//|                 VerysVeryInc.Python3.Django.TemplateTags.Math.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.TemplateTags.Math.py - Ver.3.7.14 Update:2018.03.29" |
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
### MatsuoStation.Com ###
# from django.template.defaultfilters import register

from django import template
register = template.Library()

import math
from Finance.models import Value_Test10, Value_Test20


@register.filter("change_int")
def change_int(value):
    return int(value)


@register.filter("s_code_value")
def s_code_value(gc, sc):

	# (Ver.3.7.8.OK) s_values = Value_Test10.objects.all().filter(uid__endswith=gc, s_code=sc)
	s_values = Value_Test20.objects.all().filter(uid=gc, s_code=sc)

	for v in s_values:
		sv = v.value

		return sv

@register.filter("keiyu_code_value")
def keiyu_code_value(gc, sc):

	# (Ver.3.7.8.OK) s_values = Value_Test10.objects.all().filter(uid__endswith=gc, s_code=sc)
	s_values = Value_Test20.objects.all().filter(uid=gc, s_code=sc)

	for v in s_values:
		sv = v.value - 32.1

		return sv



@register.filter("check_unit")
def check_unit(value, amount):

	try:
		# values = (value * 1.08 ) / ( amount / 100 )
		values = (value * 1.00 ) / ( amount / 100 )
		return values
	except ZeroDivisionError:
		return print("ZeroDivisionError")

	# return values

	'''
	if unit == 0:
		units = amount
	else:
		units = unit

	return units
	'''


@register.filter("red_value")
def red_value(value, rv):
	if(rv == 8):
		values = -(value)
	else:
		values = value

	return int(values)


@register.filter("notax")
def notax(value, args):
	# values = math.floor(value * args / 100)
	# values = -(-value * args / 100)
	values = round(value * args / 100, 0)
	return int(values)

@register.filter("intax")
def intax(value, args):
	if args != 0:
		values = args + value
	else:
		# values = -(-value * 0.08) + value
		values = round(value * 0.08, 0) + value

	return int(values)

	# values = math.floor(value * args / 100)
	# values = -(-value * args / 100)
	# return int(values)


@register.filter("s_tax")
def s_tax(sc, tax_value):
# def s_tax(sc):

	# if sc == "10000" or sc == "10100" or sc == "10200" or sc == "10500":
	if sc == "10000" or sc == "10100" or sc == "10200":
		return str("")
	elif tax_value > 0:
		return str("")

	else:
		return str("内")

	# return sc

@register.filter("k_tax")
def k_tax(value, args):
	values = math.floor(32.1 * args / 100)
	return int(values)

@register.filter("c_tax")
def c_tax(value, args ):

	if args != 0:
		values = args
	else:
		# values = -(-value * 0.08)
		values = round(value * 0.08, 0)

	return int(values)

@register.filter("o_tax")
def o_tax(value, args ):

	if args != 0:
		values = args
	else:
		# values = -(-value * 0.08)
		values = round(value - (value / 1.08), 0)

	return int(values)





@register.filter("minus")
def minus(value, args):
	return value - args

@register.filter("divistion")
def division(value, args):
	return value / args

@register.filter("multiplication")
def multiplication(value, args):
	return value * args
