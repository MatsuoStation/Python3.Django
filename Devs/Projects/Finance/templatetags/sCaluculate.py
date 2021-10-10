#//+------------------------------------------------------------------+
#//|  VerysVeryInc.Python3.Django.Finance.TemplateTags.sCaluculate.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.TempTags.sCal.py - Ver.3.93.23 Update:2021.10.08" |
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
def Unit_aCal(sc, am, vl, md, flag, df_high, df_reg, df_ku, df_tut, df_tuh):
# def Unit_aCal(sc, am, md):
# def Unit_Cal(sc, gc, am, vl, tax, red, md):
    # 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
    jtax = jTax(md)

    # 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
    if SC_Check(sc) == "Cash":
        sv, cTax = Cash_Cal(sc, vl)
        uc = '0'

    # ハイオク(10000)
    elif SC_Check(sc) == "OIL" and sc == '10000':
        uc = '10000'
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

        ## GAS : リスト出力　##
        df_reg_fl = df_reg.filter(items=['m_datetime', 'okayama', 'okayama_kake'])
        df_reg_md = df_reg_fl[df_reg_fl['m_datetime'] <= str(md)].tail(1)
        df_reg_len = len(df_reg_md)
        if flag == "現金":
            uc = df_reg_md.iat[df_reg_len - 1, 1]
        else:
            uc = df_reg_md.iat[df_reg_len - 1, 2]

        # (Dev) df_reg_md = df_reg_fl[df_reg_fl['m_datetime'] == '2021-10-04']
        # (Test) uc = df_reg_md
        # (OK) uc = df_reg_md.iat[df_reg_len-1, 1]
        # (OK) uc = df_reg_md.iat[0, 1]
        # uc = df_reg_fl.query('m_datetime' == '2021-10-04').at['okayama_kake']
        # uc = df_reg
        # uc = df_reg.filter(items=['A', 'E']).filter(items='2021-10-04', axis=0)
        # print(df_reg)
        # uc = '10100'
    # 軽油(10200)
    elif SC_Check(sc) == "OIL" and sc == '10200': uc = '10200'
    # 灯油特別(10500)
    elif SC_Check(sc) == "OIL" and sc == '10500': uc = '10500'

    # 油以外 : 免税軽油(10300) or 灯油(10500) or 重油(10600)含む
    elif SC_Check(sc) == "nOIL":
        sv, cTax, cAm = nOIL_Cal(sc, am, md)
        # sv, cTax, cAm = nOIL_Cal(sc, gc, am, md)
        # sv, cTax, cAm = nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md)
        # sv, cTax = nOIL_Cal(sc, vl, tax, jtax, red)
        uc = Decimal(sv / (am / 100)).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        # uc = sv

    # 例外
    else:
        uc = sc

    return uc


### 売上高 : 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収 ###
def Cash_Cal(sc, vl):
    if sc == "00000" or sc == "00001" or sc == "00002" or sc == "00003" or sc == "01100":
        sv = vl
        cTax = 0
    return sv, cTax

### 売上高 : 油以外 - 免税軽油(10300) or 灯油(10500) or 重油(10600)含む ###
def nOIL_Cal(sc, am, md):
# def nOIL_Cal(sc, gc, am, md):
    if sc != "10000" or sc != "10100" or sc != "10200":
        sv = 100
        cTax = 10
        cAm = 200

    return sv, cTax, cAm


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



