#//+------------------------------------------------------------------+
#//|             VerysVeryInc.Python3.Django.sFreee.Util.DB_sFreee.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.Util.DB.sFreee.py - Ver.3.93.8 Update:2021.09.28" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
import django
django.setup()

from Finance.models import SHARPnPOS_1501_2107, SHARPnPOS
from django.db.models import Q

### DB_sFreee ###
def DB_sFreee(self, dlb, dla):
    SnPs = SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # for q in SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb):
    #     SnPs = q

    return SnPs
