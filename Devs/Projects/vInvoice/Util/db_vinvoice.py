#//+------------------------------------------------------------------+
#//|         VerysVeryInc.Python3.Django.vInvoice.Util.DB_vInvoice.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Py3.Dj.Util.DB.vInvoice.py - Ver.3.80.32  Update:2021.01.05" |
#//+------------------------------------------------------------------+
from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20, Value_Test30

def DB_vInvoice(self, dld, dlm, bld, blm):
# def DB_vInvoice(self, dld, dlm):


    ## IVs ##
    if dld:
        IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
    else:
        IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')

    ## bIVs ##
    if bld:
        bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=bld, m_datetime__lte=blm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
    else:
        bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')

    ## lastmonths ##
    lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

    ## BFs ##
    BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

    ## VLs ##
    # VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')

    ## names ##
    names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

    # return names, IVs, lastmonths, BFs, VLs
    # return names, IVs, lastmonths, BFs
    return names, IVs, bIVs, lastmonths, BFs

'''
def DB_vValue(self, sc, m_datetime):
    if Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=sc, m_datetime__lte=m_datetime):
        v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=sc, m_datetime__lte=m_datetime)
    return v_values
'''