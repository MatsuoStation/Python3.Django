#//+------------------------------------------------------------------+
#//|                         VerysVeryInc.Python3.Django.LPG.Forms.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Python3.Dj.LPG.Forms.py - Ver.3.11.1 Update:2018.05.15" |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
from django import forms
# from django.forms import ModelForm
# from Finance.models import Name_Test


# Create your tests here.
### MatsuoStation.Com ###
class NameForm(forms.Form):
# class NameForm(ModelForm):
	nid = forms.CharField(max_length=6, required=False, label='顧客番号')
	# lastday = forms.CharField( required=False, label='締切日' )
	# deadline = forms.DateField( required=False, label='締切日' )

	# class Meta:
	#	model = Name_Test
	#	fields = ['uid']


class MyForm(forms.Form):
	# text = forms.CharField(max_length=100)
	text = forms.CharField(max_length=100, required=False, label='顧客番号')

