#//+------------------------------------------------------------------+
#//|         VerysVeryInc.Python3.Django.aInvoice.Util.DB_vInvoice.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.Util.DB.bInvoice.py - Ver.3.91.20 Update:2021.03.30" |
#//+------------------------------------------------------------------+
from Finance.models import SHARPnPOS
from django.db.models import Q

## DB_aInvoice ##
def DB_bInvoice(self, dld, dlm, bld, blm):

    ## SnP ##
    SnP = SHARPnPOS.objects.all().filter(m_datetime__gte='2015-08-01').exclude(Q(p_code='01') | Q(p_code=91) | Q(p_code=92) | Q(p_code=93)).order_by('m_datetime')
    # (r_code <> 9) SnP = SHARPnPOS.objects.all().filter(m_datetime__gte='2015-08-01', m_datetime__lte='2015-08-03').exclude(Q(p_code='01') | Q(p_code=91) | Q(p_code=92) | Q(p_code=93) | Q(r_code=9)).order_by('m_datetime')
    # SnP = SHARPnPOS.objects.all().exclude(Q(p_code=91) | Q(p_code=92) | Q(p_code=93)).order_by('m_datetime')
    # SnP = SHARPnPOS.objects.all().order_by('s_code', 'car_code', 'm_datetime')

    return SnP
