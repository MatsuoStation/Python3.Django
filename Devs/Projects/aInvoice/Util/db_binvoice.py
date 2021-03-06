#//+------------------------------------------------------------------+
#//|         VerysVeryInc.Python3.Django.aInvoice.Util.DB_vInvoice.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.Util.DB.bInvoice.py - Ver.3.91.11 Update:2021.03.05" |
#//+------------------------------------------------------------------+
from Finance.models import SHARPnPOS

## DB_aInvoice ##
def DB_bInvoice(self, dld, dlm, bld, blm):

    ## SnP ##
    SnP = SHARPnPOS.objects.all().order_by('s_code', 'car_code', 'm_datetime')

    return SnP
