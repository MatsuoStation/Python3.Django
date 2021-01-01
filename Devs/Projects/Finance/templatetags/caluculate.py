#//+------------------------------------------------------------------+
#//|   VerysVeryInc.Python3.Django.Finance.TemplateTags.Caluculate.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.Dj.TempTags.Cal.py - Ver.3.80.20 Update:2021.01.01" |
#//+------------------------------------------------------------------+
from datetime import datetime
from decimal import *

jtax10 = 0.10
jtax8 = 0.08


### 単価 : Setup　###
def Unit_Cal(v_values):
    un = 10

    return un



### 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
def jTax(m_datetime):
    # 消費税率 : 設定
    if m_datetime >= datetime.strptime("2019-10-01", '%Y-%m-%d'):
        jtax = jtax10
    else:
        jtax = jtax8
    return jtax

### S_Code : Check
def SC_Check(sc):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        scc = "Cash"
    elif sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300" or sc == "10500" or sc == "10600":
        scc = "OIL"
    elif sc != "10000" or sc != "10100" or sc != "10200" or sc != "10300" or sc != "10500" or sc != "10600":
        scc = "nOIL"
    else:
        scc = "None"
    return scc

### InCash : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def InCash_Cal(sc, value):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = value
    return sv

### 売上高 : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def Cash_Cal(sc):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = 0
        cTax = 0
    return sv, cTax

### 売上高 : ハイオク(10000) or レギュラー(10100) or 軽油(10200) or 免税軽油(10300) or 灯油(10500) or 重油(10600) ###
def OIL_Cal(sc):
    if sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300" or sc == "10500" or sc == "10600":
        sv = 0
        cTax = 0
    return sv, cTax

### 売上高 : 油以外 ###
def nOIL_Cal(sc,value,tax,jtax,red_code):
    if sc != "10000" or sc != "10100" or sc != "10200" or sc != "10300" or sc != "10500" or sc != "10600":

        # 消費税 : True
        if tax != 0:
            # 消費税 : == 四捨五入（税別価格 * 消費税率）
            if tax == Decimal(value * jtax).quantize(Decimal('1'), rounding=ROUND_HALF_UP):
                sv = value + tax
                cTax = tax
                # 赤伝票 : True
                if red_code:
                    sv = -(sv)
            # 消費税 : 不一致 - 計算間違い・POS記載
            else:
                sv = 10000000000000

    return sv, cTax

