#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.12 Update:2020.12.31" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import *

from .forms import NameForm
from .Util.deadline import DeadLine, DeadLine_List
# from .db_vinvoice import DB_vInvoice
from .Util.db_vinvoice import DB_vInvoice
from .pdf import fPDF_SS_BackImage
from Finance.models import Name_Test20
from Finance.templatetags.caluculate import jTax, SC_Check, Cash_Cal, OIL_Cal, nOIL_Cal

# jtax10 = 0.10
# jtax8 = 0.08


### vInvoice_List ###
class vInvoice_List(ListView):
	model = Name_Test20
	form_class = NameForm
	template_name = 'vlist.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post )
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Search : g_code ##
		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		## DeadLine : Setup ##
		dd_list = list()

		## * try: * dl = Ture ##
		try:
			dl = self.request.GET.get('dl', '')
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlstr.day 		# DeadLine : Day
			dld, dlm, dlb, dla = DeadLine(dd, dlstr)

			## DB : Setup ##
			names, IVs, lastmonths, BFs = DB_vInvoice(self, dld, dlm)
			context['ivs'] = IVs

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = True) ##
			try:
				if BFs:
					d_values = BFs
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=True / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			context['dlb'] = dlb
			context['dla'] = dla
			## End of LastDay : Check (dl = True) ##

			## BANK : Invoice.Format ##
			for bf in BFs:
				fPDF = bf.s_format
				context['fPDF'] = fPDF

				## Invoice.Format : Back.Image - Setup
				fURL = fPDF_SS_BackImage(fPDF)
				context['fURL'] = fURL
			## End of BANK : Invoice.Format ##

			## Cash Income : Total ##
			incash_list = list()
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values

			## Cash Value : Total ##
			total_list = list()

			## Caluculate ##
			try:
				## Select Month ##
				for iv in IVs:
					jtax = jTax(iv.m_datetime)

					'''
					# 消費税率 : 設定
					if iv.m_datetime >= datetime.strptime("2019-10-01", '%Y-%m-%d'):
						jtax = jtax10
					else:
						jtax = jtax8
					'''

					# 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
					if SC_Check(iv.s_code.uid) == "Cash":
						sv, cTax = Cash_Cal(iv.s_code.uid)
						total_list.append(sv)

					#if iv.s_code.uid == "00000" or iv.s_code.uid == "00001" or \
					#		iv.s_code.uid == "00002" or iv.s_code.uid == "00003" or iv.s_code.uid == "01100":
					#	sv = 0
					#	total_list.append(sv)

					# OIL
					elif SC_Check(iv.s_code.uid) == "OIL":
						sv, cTax = OIL_Cal(iv.s_code.uid)
						total_list.append(sv)

					# OIL以外
					elif SC_Check(iv.s_code.uid) == "nOIL":
						sv, cTax = nOIL_Cal(iv.s_code.uid, iv.value, iv.tax, jtax, iv.red_code)
						# nOIL_Cal(sc,value,tax,jtax,red_code):
						total_list.append(sv)

					#elif iv.s_code.uid != "10000" or iv.s_code.uid != "10100" or iv.s_code.uid != "10200" or \
					#	iv.s_code.uid != "10300" or iv.s_code.uid != "10500" or iv.s_code.uid != "10600":
						# 消費税 : True
					#	if iv.tax != 0:
							# 消費税 : == 四捨五入(税別価格 * 消費税率)
					#		if iv.tax == Decimal(iv.value * jtax).quantize(Decimal('1'), rounding=ROUND_HALF_UP):
					#			sv = iv.value + iv.tax
								# 赤伝票 : True
					#			if iv.red_code:
					#				sv = -(sv)
					#			total_list.append(sv)
							# 消費税 : Diff
					#		else:
					#			sv = 10000000000000
					#			total_list.append(sv)

							#''' (OK)
							#sv = iv.value + iv.tax
							#total_list.append(sv)
							#'''

					# その他 : 現金 & OIL & OIL以外
					else:
						sv = 0
						total_list.append(sv)

				## Value : Sum ##
				total_values = sum(total_list)

				## Value : Context ##
				context['total_values'] = total_values

			except Exception as e:
				print("Exception - views.py / dl=True / Caluculate  : %s" % e)
			## End of Caluculate ##

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## DB : Setup ##
			names, IVs, lastmonths, BFs = DB_vInvoice(self, "", "")

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = False) ##
			try:
				if BFs:
					d_values = BFs
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=False / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			## End of LastDay : Check (dl = False) ##

		## name : Setup ##
		for name in names:
			context['names'] = name.g_code.name

		return context

### Index(request) ###
def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post)
	else:
		form = NameForm()
	return render(request, 'vInvoice.html', {'form': form})

	# return HttpResponse("Hello vInvoice/view.py. You're at the vInvoice.")
