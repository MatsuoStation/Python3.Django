#//+------------------------------------------------------------------+
#//|              VerysVeryInc.Python3.Django.TemplateTags.vFilter.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.TempTags.vFilter.py - Ver.3.80.12 Update:2020.12.31" |
#//+------------------------------------------------------------------+
from django import template
from datetime import datetime
from decimal import *
from Finance.templatetags.caluculate import jTax, SC_Check, Cash_Cal, OIL_Cal, nOIL_Cal

register = template.Library()
jtax10 = 0.10
jtax8 = 0.08


# one_two - (OK)
@register.filter("one_two")
def one_two(one, two):
    return one, two

# check_tax - (OK)
@register.filter("check_tax")
def check_tax(tax_date_sc_red, value):
    tax_date_sc, red_code = tax_date_sc_red
    tax_date, sc = tax_date_sc
    tax_value, m_datetime = tax_date
    
    jtax = jTax(m_datetime)
    '''
    if m_datetime >= datetime.strptime("2019-10-01", '%Y-%m-%d'):
        jtax = jtax10
    else:
        jtax = jtax8
    '''

    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc)

    # if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
    #    cTax = 0
    # OIL

    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) or 免税軽油(10300) or 灯油(10500) or 重油(10600)
    elif SC_Check(sc) == "OIL":
        sv, cTax = OIL_Cal(sc)

    # elif sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300" or sc == "10500" or sc == "10600":
    #    cTax = 1

    # 油以外
    elif SC_Check(sc) == "nOIL":
        sv, cTax = nOIL_Cal(sc, value, tax_value, jtax, red_code)

    # 消費税 : == 四捨五入(税別価格 * 消費税率)
    # elif tax_value == Decimal(value * jtax).quantize(Decimal('1'), rounding=ROUND_HALF_UP):
    #    cTax = tax_value

    # その他
    else:
        cTax = 90000000000000
    return cTax

# Division - (OK)
@register.filter("divistion")
def division(value, args):
	return value / args

# Red_Value - (OK)
@register.filter("red_value")
def red_value(value, rv):
	if(rv == 8):
		values = -(value)
	else:
		values = value
	return int(values)

# s_tax - (OK)
@register.filter("s_tax")
def s_tax(sc, tax_value):
    # if OIL.SC >= 10000 AND OIL.SC <= 10600:
    if sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300" or sc == "10500" or sc == "10600":
        return str("【OIL】")
    elif tax_value > 0:
        return str("")
    else:
        return str("内")

	# if ハイオク.sc == "10000" or レギュラー.sc == "10100" or 軽油.sc == "10200" or sc == "10500":
	#if sc == "10000" or sc == "10100" or sc == "10200":
	#	return str("")
	#elif tax_value > 0:
	#	return str("")
	#else:
	#	return str("内")