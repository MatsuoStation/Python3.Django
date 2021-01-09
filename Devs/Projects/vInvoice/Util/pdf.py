#//+------------------------------------------------------------------+
#//|                 VerysVeryInc.Python3.Django.vInvoice.Util.PDF.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|"VsV.Py3.Dj.vInvoice.Util.PDF.py - Ver.3.80.71 Update:2021.01.10" |
#//+------------------------------------------------------------------+

def fPDF_SS_BackImage(fPDF):
    if fPDF == 1:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_03.png"
        # fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
    if fPDF == 2:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_1_03.png"
        # fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
    if fPDF == 11:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_03.png"
        # fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
    if fPDF == 12:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_11_03.png"
        # fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
    if fPDF == 20:
        fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_20_03.png"
        # fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_20_02.png"

    return fURL