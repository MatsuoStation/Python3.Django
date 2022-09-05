#//+------------------------------------------------------------------+
#//|             VerysVeryInc.Python3.Django.sFreee.Util.DB_sFreee.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.Util.DB.sFreee.py - Ver.3.93.32 Update:2022.09.05" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
# import django
# django.setup()

from Finance.models import SHARPnPOS_1501_2107, SHARPnPOS_2108_2207, SHARPnPOS
from django.db.models import Q

### DB_sFreee ###
def DB_sFreee(self, dlb, dla):
    ## p_code : 01.POS開始 / 10.00.''.売上高 / 20.売上回収 / 30.現金仕入 / 31.掛仕入 / 32.仕入返品 / 40.出金 / 50.棚卸 / 91.92.93.POS締
    SnPs = SHARPnPOS.objects.filter((Q(p_code='10') | Q(p_code='20') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.filter((Q(p_code='10') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnP20 = SHARPnPOS_1501_2107.objects.filter(Q(p_code='20'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP30 = SHARPnPOS.objects.filter((Q(p_code='30') | Q(p_code='31') | Q(p_code='32')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP40 = SHARPnPOS.objects.filter(Q(p_code='40'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP50 = SHARPnPOS.objects.filter(Q(p_code='50'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP90 = SHARPnPOS.objects.filter((Q(p_code='91') | Q(p_code='92') | Q(p_code='93')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.exclude(Q(p_code='01') | Q(p_code='1') | Q(p_code='20') | Q(p_code='30') | Q(p_code='31') | Q(p_code='32') | Q(p_code='40') | Q(p_code='50') | Q(p_code='91') | Q(p_code='92') | Q(p_code='93')).filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # for q in SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb):
    #     SnPs = q

    return SnPs, SnP30, SnP40, SnP50, SnP90
    # return SnPs, SnP20, SnP30, SnP40, SnP50, SnP90

def DB_sFreee_2207(self, dlb, dla):
    ## p_code : 01.POS開始 / 10.00.''.売上高 / 20.売上回収 / 30.現金仕入 / 31.掛仕入 / 32.仕入返品 / 40.出金 / 50.棚卸 / 91.92.93.POS締
    SnPs = SHARPnPOS_2108_2207.objects.filter((Q(p_code='10') | Q(p_code='20') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.filter((Q(p_code='10') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnP20 = SHARPnPOS_1501_2107.objects.filter(Q(p_code='20'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP30 = SHARPnPOS_2108_2207.objects.filter((Q(p_code='30') | Q(p_code='31') | Q(p_code='32')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP40 = SHARPnPOS_2108_2207.objects.filter(Q(p_code='40'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP50 = SHARPnPOS_2108_2207.objects.filter(Q(p_code='50'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP90 = SHARPnPOS_2108_2207.objects.filter((Q(p_code='91') | Q(p_code='92') | Q(p_code='93')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.exclude(Q(p_code='01') | Q(p_code='1') | Q(p_code='20') | Q(p_code='30') | Q(p_code='31') | Q(p_code='32') | Q(p_code='40') | Q(p_code='50') | Q(p_code='91') | Q(p_code='92') | Q(p_code='93')).filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # for q in SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb):
    #     SnPs = q

    return SnPs, SnP30, SnP40, SnP50, SnP90
    # return SnPs, SnP20, SnP30, SnP40, SnP50, SnP90

def DB_sFreee_2107(self, dlb, dla):
    ## p_code : 01.POS開始 / 10.00.''.売上高 / 20.売上回収 / 30.現金仕入 / 31.掛仕入 / 32.仕入返品 / 40.出金 / 50.棚卸 / 91.92.93.POS締
    SnPs = SHARPnPOS_1501_2107.objects.filter((Q(p_code='10') | Q(p_code='20') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.filter((Q(p_code='10') | Q(p_code='') | Q(p_code='00')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnP20 = SHARPnPOS_1501_2107.objects.filter(Q(p_code='20'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP30 = SHARPnPOS_1501_2107.objects.filter((Q(p_code='30') | Q(p_code='31') | Q(p_code='32')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP40 = SHARPnPOS_1501_2107.objects.filter(Q(p_code='40'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP50 = SHARPnPOS_1501_2107.objects.filter(Q(p_code='50'), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    SnP90 = SHARPnPOS_1501_2107.objects.filter((Q(p_code='91') | Q(p_code='92') | Q(p_code='93')), m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.exclude(Q(p_code='01') | Q(p_code='1') | Q(p_code='20') | Q(p_code='30') | Q(p_code='31') | Q(p_code='32') | Q(p_code='40') | Q(p_code='50') | Q(p_code='91') | Q(p_code='92') | Q(p_code='93')).filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # SnPs = SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb, m_datetime__lte=dla).order_by('m_datetime')
    # for q in SHARPnPOS_1501_2107.objects.all().filter(m_datetime__gte=dlb):
    #     SnPs = q

    return SnPs, SnP30, SnP40, SnP50, SnP90
    # return SnPs, SnP20, SnP30, SnP40, SnP50, SnP90
