#//+------------------------------------------------------------------+
#//|              VerysVeryInc.Python3.Django.sFreee.Util.DeadLine.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.sF.Util.DeadLine.py-Ver.3.93.7 Update:2021.09.28" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def DeadLine(dlstr):

    dlb = dlstr
    dla = dlstr + relativedelta(months=1) - timedelta(microseconds=1)

    return dlb, dla


