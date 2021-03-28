#//+------------------------------------------------------------------+
#//|              VerysVeryInc.Python3.Django.TemplateTags.bFilter.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.TempTags.bFilter.py - Ver.3.91.15 Update:2021.03.27" |
#//+------------------------------------------------------------------+
from django import template
from datetime import datetime
from decimal import *
from Finance.templatetags.bCaluculate import jTax, SC_Check, Cash_Cal, OIL_Cal, nOIL_Cal, Unit_Cal, Vl_Cal, inVl_Cal, kTax_Cal, ITm_sc_name,\
    Income_Cal, Expense_Cal
# from Finance.templatetags.caluculate import jTax, SC_Check, Cash_Cal, OIL_Cal, nOIL_Cal, Unit_Cal, Vl_Cal, inVl_Cal, kTax_Cal

from Finance.templatetags.bCaluculate import aPartner_gc_name, aPartner_fc_id, aAccount_item_id, aItems_id, aBumon_id


register = template.Library()

### ALLFreee : Setup ###
@register.filter("g_code_name")
def g_code_name(gc):
    gc_name = aPartner_gc_name(gc)
    # gc_name = "レギュラー"
    return gc_name

@register.filter("f_code_id")
def f_code_id(gc):
    fc_id = aPartner_fc_id(gc)
    # fc_id = "99999999999"
    return fc_id

@register.filter("a_item_id")
def a_item_id(ac):
    ac_id = aAccount_item_id(ac)
    # ac_id = "400267943"
    return ac_id

@register.filter("item_id")
def item_id(sc):
    item_id = aItems_id(sc)
    # item_id = sc
    return item_id

@register.filter("bumon_id")
def bumon_id(gc):
    b_id = aBumon_id(gc)
    # b_id = gc
    return b_id


### Def : Setup ###
# check_income_expense
@register.filter("check_income")
def check_income(entry, am):
    amount = Income_Cal(entry, am)
    return amount

@register.filter("check_expense")
def check_expense(entry, am):
    amount = Expense_Cal(entry, am)
    return amount

# one_two - (OK)
@register.filter("one_two")
def one_two(one, two):
    return one, two

# check_invalue - (OK)
@register.filter("check_invalue")
def check_invalue(sc_gc_am_vl_tax_red, md):
    sc_gc_am_vl_tax, red = sc_gc_am_vl_tax_red
    sc_gc_am_vl, tax = sc_gc_am_vl_tax
    sc_gc_am, vl = sc_gc_am_vl
    sc_gc, am = sc_gc_am
    sc, gc = sc_gc
    sv = inVl_Cal(sc, gc, am, vl, tax, red, md)
    return sv

# check_value - (OK)
@register.filter("check_value")
def check_value(sc_gc_am_vl_tax_red, md):
    sc_gc_am_vl_tax, red = sc_gc_am_vl_tax_red
    sc_gc_am_vl, tax = sc_gc_am_vl_tax
    sc_gc_am, vl = sc_gc_am_vl
    sc_gc, am = sc_gc_am
    sc, gc = sc_gc
    vc = Vl_Cal(sc, gc, am, vl, tax, red, md)
    return vc

# check_ktax - (OK)
@register.filter("check_ktax")
def check_ktax(sc, am):
    vc = kTax_Cal(sc, am)
    return vc
'''
def check_ktax(sc_gc_am_vl_tax_red, md):
    sc_gc_am_vl_tax, red = sc_gc_am_vl_tax_red
    sc_gc_am_vl, tax = sc_gc_am_vl_tax
    sc_gc_am, vl = sc_gc_am_vl
    sc_gc, am = sc_gc_am
    sc, gc = sc_gc
    vc = kTax_Cal(sc, gc, am, vl, tax, red, md)
    return vc
'''

# check_unit - (OK)
@register.filter("check_unit")
def check_unit(sc_gc_am_vl_tax_red, md):
    sc_gc_am_vl_tax, red = sc_gc_am_vl_tax_red
    sc_gc_am_vl, tax = sc_gc_am_vl_tax
    sc_gc_am, vl = sc_gc_am_vl
    sc_gc, am = sc_gc_am
    sc, gc = sc_gc
    un = Unit_Cal(sc, gc, am, vl, tax, red, md)
    return un

# check_tax - (OK)
@register.filter("check_tax")
def check_tax(sc_gc_am_vl_tax_red, md):
    sc_gc_am_vl_tax, red = sc_gc_am_vl_tax_red
    sc_gc_am_vl, tax = sc_gc_am_vl_tax
    sc_gc_am, vl = sc_gc_am_vl
    sc_gc, am = sc_gc_am
    sc, gc = sc_gc
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)

    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) or 免税軽油(10300)
    elif SC_Check(sc) == "OIL":
        sv, cTax, cAm = OIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        # sv, cTax = OIL_Cal(sc)
    # 油以外 : 灯油(10500) or 重油(10600)含む
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        # sv, cTax = nOIL_Cal(sc, vl, tax, jtax, red)
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
def s_tax(sc, vl):
    # if OIL.SC >= 10000 AND OIL.SC <= 10600:
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) or 免税軽油(10300)
    if sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300":
    # if sc == "10000" or sc == "10100" or sc == "10300":
    # if sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300" or sc == "10500" or sc == "10600":
        return str("")
    # elif sc == "10200":
    #    return str("【OIL】")
    # 油以外 : 灯油(10500) or 重油(10600)含む
    # elif sc == "10500" or sc == "10600":
    #    return str("（TJ）")
    elif vl > 0:
        return str("")
    else:
        return str("内")

# s_code_name - (OK)
@register.filter("s_code_name")
def s_code_name(sc):

    sc_name = ITm_sc_name(sc)
    # sc_name = "レギュラー"

    return sc_name

    '''
    <--{% for i in its %}
    {% if s.s_code == i.uid %}
     <td>{{ i.h_name }}</td>
     {% endif %}
     {% endfor %}-->
    '''