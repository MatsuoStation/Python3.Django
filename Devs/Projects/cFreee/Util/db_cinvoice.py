#//+------------------------------------------------------------------+
#//|           VerysVeryInc.Python3.Django.cFreee.Util.DB_cInvoice.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.Util.DB.cInvoice.py - Ver.3.92.25 Update:2021.08.31" |
#//+------------------------------------------------------------------+
from Finance.models import Invoice_Test20, Bank_Test20, Value_Test30, Add_Test20, SHARPnPOS
# from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20, Value_Test30, Add_Test20
from django.db.models import Q

### Google.API ###
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

## GAS : SpreadSheet ##
def GAS_SpSh(self):
    ## GAS : JSON - Setup ##
    gJsonFile = "../matsuostationapi-ca6cfa70cc81.json"

    ## GAS : SpreadSheet - Setup ##
    spsh_name = 'aFreeeAPI_PartnersList'
    ws = connect_gspread(gJsonFile, spsh_name)
    ws_list = ws.worksheets()

    ## GAS : Search ##
    nid = self.kwargs.get('nid')

    # 全行抽出 - 行検索
    all_of_lists = ws_list[0].get_all_values()
    for i in all_of_lists:
        if str(nid) == i[3]:
            Name02 = i[2]
            checkDay, PdfFormat = i[5].split(',')
            return Name02, checkDay, PdfFormat
        else:
            pass

    # 行検索
    # SC1_of_lists = ws_list[0].col_values(4)
    # SC1_of_lists_in = [s for s in SC1_of_lists if s == str(nid) in s]
    # for i in SC1_of_lists_in:
    #    return i

    ## GAS : Read ##
    # cell_value = ws_list[0].acell('A1').value
    # cell_value = "Test"

    # return cell_value

### Google.API : Connect ###
def connect_gspread(jsonf, spsh):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)

    SPREADSHEET_KEY = spsh

    worksheet = gc.open(SPREADSHEET_KEY)
    return worksheet

## DB_cInvoice ##
def DB_cInvoice(self, dld, dlm, bld, blm):
# def DB_vInvoice(self, dld, dlm):

    ## IVs ##
    if dld:
        IVs = SHARPnPOS.objects.exclude(Q(p_code=91), Q(p_code=92), Q(p_code=93), Q(p_code=1), Q(p_code=50),Q(p_code=31)).filter(g_code__exact=self.kwargs.get('nid'), r_code=9, m_datetime__gte=dld, m_datetime__lte=dlm).order_by('s_code', 'car_code', 'm_datetime')
    else:
        IVs = SHARPnPOS.objects.exclude(Q(p_code=91), Q(p_code=92), Q(p_code=93), Q(p_code=1), Q(p_code=50),Q(p_code=31)).filter(g_code__exact=self.kwargs.get('nid'), r_code=9).order_by('s_code', 'car_code', 'm_datetime')

    # (Def) IVs = SHARPnPOS.objects.exclude(Q(p_code=91), Q(p_code=92), Q(p_code=93), Q(p_code=1), Q(p_code=50), Q(p_code=31)).filter(g_code__exact=self.kwargs.get('nid'), p_code=10, r_code=9).order_by('s_code', 'car_code', 'm_datetime')
    # if dld:
        # IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('s_code', 'car_code', 'm_datetime')
    # else:
        # IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('s_code', 'car_code', 'm_datetime')

    ## bIVs ##
    if bld:
        bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=bld, m_datetime__lte=blm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
    else:
        bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')

    ## lastmonths ##
    # lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')
    lastmonths = SHARPnPOS.objects.all().filter(g_code=self.kwargs.get('nid')).values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

    ## BFs ##
    BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

    ## VLs ##
    # VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')

    ## names ##
    # names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

    # return names, IVs, lastmonths, BFs, VLs
    # return names, IVs, lastmonths, BFs
    # return names, IVs, bIVs, lastmonths, BFs
    return IVs, bIVs, lastmonths, BFs

## DB_Address ##
def DB_Address(self):

    ## ADs ##
    ADs = Add_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

    return ADs

'''
def DB_vValue(self, sc, m_datetime):
    if Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=sc, m_datetime__lte=m_datetime):
        v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=sc, m_datetime__lte=m_datetime)
    return v_values
'''