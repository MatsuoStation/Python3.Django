#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Forms.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Invoice.Forms.py - Ver.3.5.6 Update:2018.03.14" |
#//+------------------------------------------------------------------+
from django import forms

# Create your tests here.
### MatsuoStation.Com ###
class MyForm(forms.Form):
	# text = forms.CharField(max_length=100)
	text = forms.CharField(max_length=100, required=False, label='顧客番号')

