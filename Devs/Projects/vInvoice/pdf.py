#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.vInvoice.PDF.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.vInvoice.PDF.py - Ver.3.80.7 Update:2020.12.28" |
#//+------------------------------------------------------------------+

def fPDF_SS_BackImage(fPDF):
    if fPDF == 0:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
    if fPDF == 10:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
    if fPDF == 20:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_20_02.png"

    return fURL