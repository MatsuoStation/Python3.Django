#//+------------------------------------------------------------------+
#//|   VerysVeryInc.Python3.Django.Finance.TemplateTags.Caluculate.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.TempTags.Cal.py - Ver.3.90.8 Update:2021.01.19" |
#//+------------------------------------------------------------------+
from datetime import datetime
from decimal import *
from datetime import datetime

from Finance.models import Value_Test30, Items_Test10

jtax10 = 0.10
jtax8 = 0.08


### 税込金額 : Setup　###
def inVl_Cal(sc, gc, am, vl, tax, red, md):
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)
    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
        vc = sv
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200)
    # elif SC_Check(sc) == "OIL" or (vl == 0 and sc == "10500"):
    elif SC_Check(sc) == "OIL":
        uc = Unit_Cal(sc, gc, am, vl, tax, red, md)
        vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        tc = Tax_Cal(vc, tax, jtax, "OIL")
        vc = vc + tc
        if red:
            vc = -(vc)
    # 灯油特別(10500) : 内税
    elif vl == 0 and sc == "10500":
        uc = Unit_Cal(sc, gc, am, vl, tax, red, md)
        vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if red:
            vc = -(vc)
    # 油以外 : 免税軽油(10300) or 灯油(10500) or 重油(10600)含む
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        vc = sv
        # if red:
        #    vc = -(vc)
    else:
        vc = sc
    return vc

### 金額 : Setup　###
def Vl_Cal(sc, gc, am, vl, tax, red, md):
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)
    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
        vc = sv
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) : 灯油特別(10500)
    elif SC_Check(sc) == "OIL" or (vl == 0 and sc == "10500"):
        uc = Unit_Cal(sc, gc, am, vl, tax, red, md)
        vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if red:
            vc = -(vc)
    # 油以外 : 免税軽油(10300) or 灯油(10500) or 重油(10600)含む
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        vc = sv - cTax
        # if red:
        #    vc = -(vc)
    else:
        vc = sc
    return vc

### 軽油税 : Setup　###
def kTax_Cal(sc, am):
# def kTax_Cal(sc, gc, am, vl, tax, red, md):
    kt = Decimal(float(32.1) * (am / 100)).quantize(Decimal('1'), rounding=ROUND_DOWN)
    return kt

### 単価 : Setup　###
def Unit_Cal(sc, gc, am, vl, tax, red, md):
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)

    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
        uc = 0
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) : 灯油特別(10500)
    elif SC_Check(sc) == "OIL" or (vl == 0 and sc == "10500"):
        if Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, m_datetime__lte=md), 0)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date01__lte=md), 1)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date02__lte=md), 2)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date03__lte=md), 3)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date04__lte=md), 4)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date05__lte=md), 5)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date06__lte=md), 6)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date07__lte=md), 7)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date08__lte=md), 8)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date09__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date09__lte=md), 9)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date10__lte=md), 10)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date11__lte=md), 11)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date12__lte=md), 12)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date13__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date13__lte=md), 13)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date14__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date14__lte=md), 14)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date15__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date15__lte=md), 15)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date16__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date16__lte=md), 16)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date17__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date17__lte=md), 17)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date18__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date18__lte=md), 18)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date19__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date19__lte=md), 19)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date20__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date20__lte=md), 20)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date21__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date21__lte=md), 21)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date22__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date22__lte=md), 22)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date23__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date23__lte=md), 23)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date24__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date24__lte=md), 24)
            uc = k_tax(sc, uc)
        elif Value_Test30.objects.all().filter(uid=gc, s_code=sc, date25__lte=md):
            uc = Unit_His(Value_Test30.objects.all().filter(uid=gc, s_code=sc, date25__lte=md), 25)
            uc = k_tax(sc, uc)
        # None OIL Value
        else:
            uc = sc
    # 油以外 : 免税軽油(10300) or 灯油(10500) or 重油(10600)含む
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        # sv, cTax = nOIL_Cal(sc, vl, tax, jtax, red)
        uc = Decimal(sv/(am/100)).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
    else:
        uc = sc
    # uc = sc
    return uc

### 単価 : SS.History ###
def Unit_His(v30, hv):
    v_values = v30
    for v in v_values:
        if hv == 0: uh = v.value
        elif hv == 1: uh = v.value01
        elif hv == 2: uh = v.value02
        elif hv == 3: uh = v.value03
        elif hv == 4: uh = v.value04
        elif hv == 5: uh = v.value05
        elif hv == 6: uh = v.value06
        elif hv == 7: uh = v.value07
        elif hv == 8: uh = v.value08
        elif hv == 9: uh = v.value09
        elif hv == 10:uh = v.value10
        elif hv == 11:uh = v.value11
        elif hv == 12:uh = v.value12
        elif hv == 13:uh = v.value13
        elif hv == 14:uh = v.value14
        elif hv == 15:uh = v.value15
        elif hv == 16:uh = v.value16
        elif hv == 17:uh = v.value17
        elif hv == 18:uh = v.value18
        elif hv == 19:uh = v.value19
        elif hv == 20:uh = v.value20
        elif hv == 21:uh = v.value21
        elif hv == 22:uh = v.value22
        elif hv == 23:uh = v.value23
        elif hv == 24:uh = v.value24
        elif hv == 25:uh = v.value25

        else: uh = 99999999
    return uh

### 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
def jTax(m_datetime):
    # 消費税率 : 設定
    if m_datetime >= datetime.strptime("2019-10-01", '%Y-%m-%d'):
        jtax = jtax10
    else:
        jtax = jtax8
    return jtax

### 消費税計算 ###
def Tax_Cal(vl, tax, jtax, tag):
    if tag == "nOIL":
        tc = (vl + tax) - Decimal((vl + tax)/(1+jtax)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    elif tag == "OIL":
        tc = Decimal(float(vl) * jtax).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    elif tag == "uTax":
        tc = Decimal(float(vl) - float(vl) / (1+jtax)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    else:
        tc = 0

    return tc

### S_Code : Check
def SC_Check(sc):
    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        scc = "Cash"
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200)
    elif sc == "10000" or sc == "10100" or sc == "10200":
        scc = "OIL"
    # 油以外 - 免税軽油(10300) or 灯油(10500) or 重油(10600)含む
    elif sc != "10000" or sc != "10100" or sc != "10200":
        scc = "nOIL"
    # その他
    else:
        scc = "None"
    return scc

### InCash : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def InCash_Cal(sc, value):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = value
    return sv

### 売上高 : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def Cash_Cal(sc, vl):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = vl
        cTax = 0
    return sv, cTax

### 売上高 : ハイオク(10000) or レギュラー(10100) or 軽油(10200) : 灯油特別(10500) ###
def OIL_Cal(sc, gc, am, vl, tax, jtax, red, md):
# def OIL_Cal(sc):
    if sc == "10000" or sc == "10100" or sc == "10200" or (vl == 0 and sc == "10500"):
        uc = Unit_Cal(sc, gc, am, vl, tax, red, md)
        vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if red:
            vc = -(vc)
            am = -(am)
        sv = vc
        tc = Tax_Cal(vc, tax, jtax, "OIL")
        cTax = tc
        # cTax = 0
        cAm = am
    return sv, cTax, cAm

### 売上高 : 油以外 - 免税軽油(10300) or 灯油(10500) or 重油(10600)含む ###
def nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md):
# def nOIL_Cal(sc, vl, tax, jtax, red):
    if sc != "10000" or sc != "10100" or sc != "10200":

        # 消費税 : True
        if tax != 0:
            # 消費税 : == (税込金額:value + tax) - (四捨五入:(税込金額:value + tax）/ (1 + jTax))
            if tax == Tax_Cal(vl, tax, jtax, "nOIL"):
            # if tax == (value + tax) - Decimal((value + tax)/(1+jtax)).quantize(Decimal('1'), rounding=ROUND_HALF_UP):
            # 消費税 : == 四捨五入（税別価格 * 消費税率）
            # if tax == Decimal(value * jtax).quantize(Decimal('1'), rounding=ROUND_HALF_UP):
                sv = vl + tax
                cTax = tax
                # 赤伝票 : True
                if red:
                    sv = -(sv)
                    cTax = -(cTax)
                    am = -(am)
                #    sv = -(vl-tax)
                cAm = am
            # 消費税 : 不一致 - 計算間違い・POS記載
            else:
                sv = 10000000000000
                cTax = 10000000000000
                cAm = 10000000000000

        # 消費税 : False - 灯油
        elif tax == 0 and sc == "10500":
            # 灯油(10500)
            sv, cTax, cAm = uOIL_Cal(sc, gc, am, vl, tax, jtax, red, md) # （内税）uOIL_Calと連動
            # sv = 0      # OIL_Calと連動
            # cTax = 0    # OIL_Calと連動

        # 消費税 : False - その他
        else:
            sv = 99999999
            cTax = 99999999
            cAm = 99999999

    return sv, cTax, cAm

### 売上高（内税金） : 灯油特別(10500) ###
def uOIL_Cal(sc, gc, am, vl, tax, jtax, red, md):
    if vl == 0 and sc == "10500":
        uc = Unit_Cal(sc, gc, am, vl, tax, red, md)
        vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        if red:
            vc = -(vc)
            am = -(am)
        sv = vc
        tc = Tax_Cal(vc, tax, jtax, "uTax")
        cTax = tc
        # cTax = 0
        cAm = am
    return sv, cTax, cAm

### 軽油税 : 設定 ###
def k_tax(sc, ut):
    if sc == "10200":
        kt = ut - 32.1
    else:
        kt = ut
    return kt

### 商品名 : 設定　###
def ITm_sc_name(sc):
    ## 商品DB ##
    ITm = Items_Test10.objects.all().filter(uid=sc).order_by('uid')

    for it in ITm:
        if sc == it.uid:
            sc_hname = it.h_name
        else:
            sc_hname = "No_Items_DB"
    # sc_hname = "Thank you"

    return sc_hname

