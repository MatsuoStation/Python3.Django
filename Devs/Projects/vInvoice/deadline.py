#//+------------------------------------------------------------------+
#//|                 VerysVeryInc.Python3.Django.vInvoice.DeadLine.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Py3.Dj.vInvoice.DeadLine.py - Ver.3.80.6 Update:2020.12.28" |
#//+------------------------------------------------------------------+
from datetime import timedelta
from dateutil.relativedelta import relativedelta

def DeadLine(dd, dlstr):
    if dd == 20 or dd == 25:
        dld = dlstr + timedelta(days=1) - relativedelta(months=1)
        dlm = dlstr + timedelta(days=1) - timedelta(microseconds=1)
        bld = dld - relativedelta(months=1)
        blm = dlm - relativedelta(months=1)
    else:
        dt = dlstr - relativedelta(months=1)
        dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
        dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)
        bld = dt - timedelta(days=dt.day) + timedelta(days=1)
        blm = bld + relativedelta(months=1) - timedelta(microseconds=1)

    dlb = dlstr + timedelta(days=1) - relativedelta(months=1)
    dla = dlstr + timedelta(days=1) - timedelta(microseconds=1)

    return dld, dlm, dlb, dla

def DeadLine_List(d, dd, dmm):
    dv = d.check_day

    if dv == 25:
        if dd >= 25:
            dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
        else:
            dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
    elif dv == 20:
        if dd >= 20:
            dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) + timedelta(days=dv - 1)
        else:
            dls = (dmm - timedelta(days=dd - 1)) + timedelta(days=dv - 1)
    else:
        dls = (dmm - timedelta(days=dd - 1)) + relativedelta(months=1) - timedelta(days=1)

    return dls
