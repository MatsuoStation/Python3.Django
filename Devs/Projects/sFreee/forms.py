#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.sFreee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.sFreee.Views.py - Ver.3.93.5 Update:2021.08.27" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
from django import forms
from django.forms import ModelForm

# Create your tests here.
### MatsuoStation.Com ###
class DateForm(forms.Form):
	mdate = forms.DateField(input_formats=["%Y-%m"], label='決算月')

class NameForm(forms.Form):
	nid = forms.CharField(max_length=5, required=False, label='顧客番号')
