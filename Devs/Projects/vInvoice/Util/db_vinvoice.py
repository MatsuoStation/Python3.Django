#//+------------------------------------------------------------------+
#//|         VerysVeryInc.Python3.Django.vInvoice.Util.DB_vInvoice.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Py3.Dj.DB.Util.vInvoice.py - Ver.3.80.9 Update:2020.12.29" |
#//+------------------------------------------------------------------+
from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20

def DB_vInvoice(self, dld, dlm):

    ## IVx ##
    if dld:
        IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld,m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
    else:
        IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')

    ## lastmonths ##
    lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

    ## BFs ##
    BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

    ## names ##
    names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

    return names, IVs, lastmonths, BFs