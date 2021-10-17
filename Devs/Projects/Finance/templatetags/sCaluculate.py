#//+------------------------------------------------------------------+
#//|  VerysVeryInc.Python3.Django.Finance.TemplateTags.sCaluculate.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.TempTags.sCal.py - Ver.3.93.27 Update:2021.10.18" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
from datetime import datetime
from decimal import *

### Google.API ###
from .Connect_GSpread import connect_gspread
import pandas as pd
from datetime import timedelta

jtax10 = 0.10
jtax8 = 0.08

## GAS : aValue.SpreadSheet - Setup ##
'''
try:
    aVspsh_name = "aValue_Okayama"
    ws_aV = connect_gspread(aVspsh_name)

    ws_high = ws_aV.worksheet('High')
    df_high = pd.DataFrame(ws_high.get_all_values());

    ws_reg = ws_aV.worksheet('Reg')
    df_reg = pd.DataFrame(ws_reg.get_all_values());
    df_reg.columns = list(df_reg.loc[0, :]);
    df_reg.drop(0, inplace=True);
    df_reg.reset_index(inplace=True)
    df_reg.drop('index', axis=1, inplace=True)

    ws_ku = ws_aV.worksheet('Ku')
    df_ku = pd.DataFrame(ws_ku.get_all_values())
    ws_tut = ws_aV.worksheet('TuT')
    df_tut = pd.DataFrame(ws_tut.get_all_values())
    ws_tuh = ws_aV.worksheet('TuH')
    df_tuh = pd.DataFrame(ws_tuh.get_all_values())
except:
    print("Exception - views.py / aValue.SpSh  : %s" % e)
'''

'''
aVspsh_name = "aValue_Okayama"
ws_aV = connect_gspread(aVspsh_name)

ws_high = ws_aV.worksheet('High')
df_high = pd.DataFrame(ws_high.get_all_values())

ws_reg = ws_aV.worksheet('Reg')
df_reg = pd.DataFrame(ws_reg.get_all_values()) ; df_reg.columns = list(df_reg.loc[0, :]) ; df_reg.drop(0, inplace=True) ; df_reg.reset_index(inplace=True)
df_reg.drop('index', axis=1, inplace=True)

ws_ku = ws_aV.worksheet('Ku')
df_ku = pd.DataFrame(ws_ku.get_all_values())
ws_tut = ws_aV.worksheet('TuT')
df_tut = pd.DataFrame(ws_tut.get_all_values())
ws_tuh = ws_aV.worksheet('TuH')
df_tuh = pd.DataFrame(ws_tuh.get_all_values())
'''

### 数量 : Setup ###
def Amount_Cal(am):
    aAm = Decimal(am/100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return aAm

### 旧単価 / 旧金額 / 旧税金 : Setup ###
def Unit_oCal(am, un, vl, tax):
    if am != 0:
        oUc = Decimal((vl+tax) / (am/100)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    else:
        oUc = un
    oVl = vl
    oTax = tax

    return oUc, oVl, oTax

### aValue.単価 : Setup　###
# def Unit_aCal(sc, am, md, flag):
# def Unit_aCal(sc, am, md, ws_aV):
def Unit_aCal(sc, am, un, vl, tax, red, md, flag, df_high, df_reg, df_ku, df_tut, df_tuh, df_aoil):
# def Unit_aCal(sc, am, un, vl, tax, md, flag, df_high, df_reg, df_ku, df_tut, df_tuh):
# def Unit_aCal(sc, am, md):
# def Unit_Cal(sc, gc, am, vl, tax, red, md):
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)

    ## 旧単価 : Check ##
    oUc_c, oVl_c, oTax_c = Unit_oCal(am, un, vl, tax)

    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
        uc = '0'
        vc = vl
        tc = '0'

    # ハイオク(10000)
    elif SC_Check(sc) == "OIL" and sc == '10000':
        ## GAS : High出力　##
        df_high_fl = df_high.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_high_md = df_high_fl[df_high_fl['m_datetime'] <= str(md)].tail(1)
        df_high_len = len(df_high_md)
        if flag == "現金":
            uc = df_high_md.iat[df_high_len - 1, 1]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)
        else:
            uc = df_high_md.iat[df_high_len - 1, 2]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)

        tc = Tax_aCal(vc, jtax)
        # uc = '10000'
        # vc = vl
        # tc = '10000'

    # レギュラー(10100)
    elif SC_Check(sc) == "OIL" and sc == '10100':
        ## GAS : DataFrame ##
        '''
        ws_reg = ws_aV.worksheet('Reg')
        df_reg = pd.DataFrame(ws_reg.get_all_values());
        df_reg.columns = list(df_reg.loc[0, :]);
        df_reg.drop(0, inplace=True);
        df_reg.reset_index(inplace=True)
        df_reg.drop('index', axis=1, inplace=True)
        '''

        ## GAS : Reg出力　##
        df_reg_fl = df_reg.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_reg_md = df_reg_fl[df_reg_fl['m_datetime'] <= str(md)].tail(1)
        df_reg_len = len(df_reg_md)
        if flag == "現金":
            uc = df_reg_md.iat[df_reg_len - 1, 1]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)
        else:
            uc = df_reg_md.iat[df_reg_len - 1, 2]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)

        tc = Tax_aCal(vc, jtax)

        # (Dev) df_reg_md = df_reg_fl[df_reg_fl['m_datetime'] == '2021-10-04']
        # (Test) uc = df_reg_md
        # (OK) uc = df_reg_md.iat[df_reg_len-1, 1]
        # (OK) uc = df_reg_md.iat[0, 1]
        # uc = df_reg_fl.query('m_datetime' == '2021-10-04').at['okayama_kake']
        # uc = df_reg
        # uc = df_reg.filter(items=['A', 'E']).filter(items='2021-10-04', axis=0)
        # print(df_reg)
        # uc = '10100'
        # vc = vl
        # tc = '10100'

    # 軽油(10200)
    elif SC_Check(sc) == "OIL" and sc == '10200':
        ## GAS : Ku出力　##
        df_ku_fl = df_ku.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_ku_md = df_ku_fl[df_ku_fl['m_datetime'] <= str(md)].tail(1)
        df_ku_len = len(df_ku_md)
        if flag == "現金":
            uc = df_ku_md.iat[df_ku_len - 1, 1]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)
        else:
            uc = df_ku_md.iat[df_ku_len - 1, 2]
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)

        tc = Tax_aCal(vc, jtax)
        # uc = '10200'
        # vc = vl
        # tc = '10200'

    # 免税軽油(10300)
    elif SC_Check(sc) == "OIL" and sc == '10300':
        ## GAS : Ku出力　##
        df_ku_fl = df_ku.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_ku_md = df_ku_fl[df_ku_fl['m_datetime'] <= str(md)].tail(1)
        df_ku_len = len(df_ku_md)
        # print(df_ku.dtypes)

        aV_mKu = df_ku_md.iat[df_ku_len - 1, 1] - 32.1
        aV_mKu_Kake = df_ku_md.iat[df_ku_len - 1, 2] - 32.1

        if flag == "現金":
            if aV_mKu < oUc_c:
                uc = aV_mKu_Kake
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            else:
                uc = aV_mKu
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            # uc = df_ku_md.iat[df_ku_len - 1, 1] - 32.1
        else:
            if aV_mKu < oUc_c:
                uc = aV_mKu_Kake
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            else:
                uc = aV_mKu
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            # uc = df_ku_md.iat[df_ku_len - 1, 2] - 32.1

        tc = Tax_aCal(vc, jtax)
        # uc = '10300'
        # vc = vl
        # tc = '10300'

    # 灯油特別(10500)
    elif SC_Check(sc) == "nOIL" and sc == '10500':
        ## GAS : TuT（灯油店頭）出力　##
        df_tut_fl = df_tut.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_tut_md = df_tut_fl[df_tut_fl['m_datetime'] <= str(md)].tail(1)
        df_tut_len = len(df_tut_md)

        ## GAS : TuH（灯油配達）出力　##
        df_tuh_fl = df_tuh.filter(items=['m_datetime', 'Okayama', 'Okayama_Kake'])
        df_tuh_md = df_tuh_fl[df_tuh_fl['m_datetime'] <= str(md)].tail(1)
        df_tuh_len = len(df_tuh_md)

        aV_TuT = df_tut_md.iat[df_tut_len - 1, 1]
        aV_TuT_Kake = df_tut_md.iat[df_tut_len - 1, 2]
        aV_TuH = df_tuh_md.iat[df_tuh_len - 1, 1]
        aV_TuH_Kake = df_tuh_md.iat[df_tuh_len - 1, 2]


        if flag == "現金":
            if aV_TuT < oUc_c:
                uc = aV_TuH
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            else:
                uc = aV_TuT
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            # uc = df_tut_md.iat[df_tut_len - 1, 1]
        else:
            if aV_TuT_Kake < oUc_c:
                uc = aV_TuH_Kake
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            else:
                uc = aV_TuT_Kake
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)

            aV_TuT = df_tut_md.iat[df_tut_len - 1, 2]
            if aV_TuT < oUc_c:
                uc = df_tuh_md.iat[df_tut_len - 1, 2]
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            else:
                uc = df_tut_md.iat[df_tut_len - 1, 2]
                vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
                if red:
                    vc = -(vc)
            # uc = df_tut_md.iat[df_tut_len - 1, 2]

        tc = Tax_aCal(vc, jtax)
        # uc = '10500'
        # vc = vl
        # tc = '10500'

    # A重油(10600) : 配達のみ
    elif SC_Check(sc) == "nOIL" and sc == '10600':
        ## GAS : Aoil出力　##
        df_aoil_fl = df_aoil.filter(items=['m_datetime', 'Okayama_inTax', 'Okayama_Kake'])
        df_aoil_md = df_aoil_fl[df_aoil_fl['m_datetime'] <= str(md)].tail(1)
        df_aoil_len = len(df_aoil_md)
        if flag == "現金":
            uc = df_aoil_md.iat[df_aoil_len - 1, 1] + 10
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)

        else:
            uc = df_aoil_md.iat[df_aoil_len - 1, 2] + 10
            vc = Decimal(uc * (am / 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            if red:
                vc = -(vc)

        tc = Tax_aCal(vc, jtax)
        # uc = '10600'
        # vc = vl
        # tc = '10600'


    # 油以外 : 灯油(10500) or 重油(10600)を除く
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, am, vl, tax, red, md)
        # sv, cTax, cAm = nOIL_Cal(sc, gc, am, md)
        # sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        # sv, cTax = nOIL_Cal(sc, vl, tax, jtax, red)
        uc = Decimal(sv / (am / 100)).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        # uc = sv
        vc = sv
        tc = Tax_aCal(vc, jtax)
        # tc = 9999


    # 例外
    else:
        uc = sc
        vc = vl
        tc = tax

    return uc, vc, tc


### 売上高 : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def Cash_Cal(sc, vl):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = vl
        cTax = 0
    return sv, cTax

### 売上高 : 油以外 - 灯油(10500) or 重油(10600)含む ###
def nOIL_Cal(sc, am, vl, tax, red, md):
# def nOIL_Cal(sc, gc, am, md):
    if sc != "10000" or sc != "10100" or sc != "10200" or sc != "10300":
        # 消費税 : True
        if tax != 0 or vl != 0:
            sv = vl + tax
            cTax = tax
            # 赤伝票 : True
            if red:
                sv = -(sv)
                cTax = -(cTax)
                am = -(am)
            cAm = am

        # 消費税 : False
        else:
            sv = 999999999
            cTax = 999999999
            cAm = 999999999

        # sv = 100
        # cTax = 10
        # cAm = 200

    return sv, cTax, cAm

### 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
def jTax(m_datetime):
    # 消費税率 : 設定
    if m_datetime >= datetime.strptime("2019-10-01", '%Y-%m-%d'):
        jtax = jtax10
    else:
        jtax = jtax8
    return jtax

### 消費税計算 ###
def Tax_aCal(vc, jtax):
    tc = Decimal(float(vc) - float(vc) / (1+jtax)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    # tc = 'TaxaCal'
    return tc


### S_Code : Check
def SC_Check(sc):
    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        scc = "Cash"
    # ハイオク(10000) or レギュラー(10100) or 軽油(10200) or 免税軽油(10300)
    elif sc == "10000" or sc == "10100" or sc == "10200" or sc == "10300":
        scc = "OIL"
    # 油以外 - 灯油(10500) or 重油(10600)含む
    elif sc != "10000" or sc != "10100" or sc != "10200" or sc != "10300":
        scc = "nOIL"
    # その他
    else:
        scc = "None"
    return scc



