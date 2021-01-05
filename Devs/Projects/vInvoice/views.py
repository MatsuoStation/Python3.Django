#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.45 Update:2021.01.06" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import *

from .forms import NameForm
from .Util.deadline import DeadLine, DeadLine_List
# from .db_vinvoice import DB_vInvoice
from .Util.db_vinvoice import DB_vInvoice, DB_Address
from .Util.pdf import  fPDF_SS_BackImage
from Finance.models import Name_Test20
from Finance.templatetags.caluculate import jTax, SC_Check, InCash_Cal, Cash_Cal, OIL_Cal, nOIL_Cal, kTax_Cal, inVl_Cal

## PDF ##
from django.template.loader import get_template
import io
from xhtml2pdf import pisa


### PDF_List ###
class PDF_List(ListView):
	model = Name_Test20
	template_name = 'pdf_vlist.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Names ##
		names = self.request.GET.get('names')
		context['names'] = names
		gid = self.kwargs.get('nid')
		context['gid'] = gid

		## Cash Income : Total ##
		incash_vl = self.request.GET.get('incash')
		## Before : Total ##
		btotal_vl = self.request.GET.get('btotal')
		## Total : Uriage ##
		total_vl = self.request.GET.get('total')
		## Slip : Total ##
		slip_vl = self.request.GET.get('slip')
		## nTax : Total ##
		ntax_vl = self.request.GET.get('ntax')
		## Tax : Total ##
		tax_vl = self.request.GET.get('tax')
		## Ku_Tax : Total ##
		ku_tx = self.request.GET.get('ktax')


		## * try: * dl = Ture ##
		try:
			## Invoice.Format : Back.Image - Setup
			fPDF = self.request.GET.get('fm')
			fPDF = int(fPDF)
			fURL = fPDF_SS_BackImage(fPDF)
			context['fURL'] = fURL

			## vInvoice_List ##
			dl = self.request.GET.get('dl', '')
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlstr.day  # DeadLine : Day
			dld, dlm, dlb, dla, bld, blm = DeadLine(dd, dlstr)
			dlaa = dla + timedelta(days=1)
			dldd = dld + timedelta(days=1)

			mSS = datetime.strftime(dlaa, '%-m')
			dSS = datetime.strftime(dla, '%-d')
			deSS = datetime.strftime(dld, '%-d')
			context['mSS'] = mSS
			context['dSS'] = dSS
			context['deSS'] = deSS
			context['dlaa'] = dlaa

			## DB : Setup ##
			names, IVs, bIVs, lastmonths, BFs = DB_vInvoice(self, dld, dlm, bld, blm)
			ADs = DB_Address(self)

			## Address : Setup ##
			for ad in ADs:
				zipcode = ad.postal_code
				address = ad.address
				context['zipcode'] = zipcode
				context['address'] = address

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

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

			## Cash Income : Total ##
			# incash_vl = self.request.GET.get('incash')

			# incash_list = list()
			# for iv in IVs:
			#	if SC_Check(iv.s_code.uid) == "Cash":
			#		sv = InCash_Cal(iv.s_code.uid, iv.value)
			#		incash_list.append(sv)

			## Uriage Value : Total ##


			## Caluculate ##
			try:
				## Select Month ##
				for iv in IVs:
					# 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
					jtax = jTax(iv.m_datetime)

				## Value : Sum ##
				# incash_vl = sum(incash_list)

				## Value : Context ##
				context['incash_vl'] = incash_vl
				context['btotal_vl'] = btotal_vl
				context['total_vl'] = total_vl
				context['slip_vl'] = slip_vl
				context['ntax_vl'] = ntax_vl
				context['tax_vl'] = tax_vl
				context['ku_tx'] = ku_tx

			except Exception as e:
				print("Exception - views.py - PDF / dl=True / Caluculate  : %s" % e)
			## End of Caluculate ##

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py - PDF / dl=False  : %s" % e)

		## Paginator : Setup ##
		paginator = Paginator(IVs, 30)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1
		try:
			IVs = paginator.page(page)
		except(EmptyPage, InvalidPage):
			IVs = paginator.page(1)
		context['ivs'] = IVs


		return context

	def render_to_response(self, context):
		html = get_template(self.template_name).render(self.get_context_data())
		result = io.BytesIO()

		## vInvoice_List ##
		gid = self.kwargs.get('nid')
		dl = self.request.GET.get('dl', '')
		dlstr = datetime.strptime(dl, "%Y-%m-%d").date()

		pdf = pisa.pisaDocument(
			io.BytesIO(html.encode("UTF-8")),
			result,
			encoding='utf-8',
		)

		if not pdf.err:
			response = HttpResponse(result.getvalue(), content_type='application/pdf')
			response['Content-Disposition'] = "inline; filename=%s_%s.pdf" % (gid, dlstr)
			return response
			# return HttpResponse(result.getvalue(), content_type='application/pdf')
		return None

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
			dld, dlm, dlb, dla, bld, blm = DeadLine(dd, dlstr)
			# dld, dlm, dlb, dla = DeadLine(dd, dlstr)

			## DB : Setup ##
			names, IVs, bIVs, lastmonths, BFs = DB_vInvoice(self, dld, dlm, bld, blm)
			# names, IVs, lastmonths, BFs = DB_vInvoice(self, dld, dlm)
			# names, IVs, lastmonths, BFs, VLs = DB_vInvoice(self, dld, dlm)

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

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

			### PDF : Link ##
			PDF_Link = "../PDF/%s/" % self.kwargs.get('nid')
			context['pLink'] = PDF_Link

			## Cash Income : Total ##
			incash_list = list()
			for iv in IVs:
				if SC_Check(iv.s_code.uid) == "Cash":
					sv = InCash_Cal(iv.s_code.uid, iv.value)
					incash_list.append(sv)

			## Uriage Value : Total ##
			slip_list = list()
			ntax_list = list()
			tax_list = list()

			bntax_list = list()
			btax_list = list()
			bku_tx_list = list()

			high_am_list = list()
			high_list = list()
			reg_am_list = list()
			reg_list = list()
			ku_am_list = list()
			ku_list = list()
			ku_tx_list = list()
			tu_am_list = list()
			tu_list = list()

			noil_list = list()

			## Caluculate ##
			try:
				## Select Month ##
				for iv in IVs:
					# 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
					jtax = jTax(iv.m_datetime)

					# 現金関係 or 小切手関係 or 振込関係 or 相殺関係 or 売掛回収
					if SC_Check(iv.s_code.uid) == "Cash":
						sv, cTax = Cash_Cal(iv.s_code.uid, iv.value)
						if sv:
							slip_list.append(0)

					# OIL
					elif SC_Check(iv.s_code.uid) == "OIL":
						sv, cTax, cAm = OIL_Cal(iv.s_code.uid, iv.g_code.uid, iv.amount, iv.value, iv.tax, jtax, iv.red_code, iv.m_datetime)
						# sv, cTax = OIL_Cal(iv.s_code.uid)
						# OIL_Cal(sc, gc, am, vl, tax, red, md):
						# total_list.append(sv+cTax)
						ntax_list.append(sv)
						tax_list.append(cTax)

						if iv.s_code.uid == "10000":
							high_am_list.append(cAm/100)
							high_list.append(sv)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)
						elif iv.s_code.uid == "10100":
							reg_am_list.append(cAm/100)
							reg_list.append(sv)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)
						elif iv.s_code.uid == "10200":
							ku_am_list.append(cAm/100)
							ku_list.append(sv)
							kc_tax = kTax_Cal(iv.s_code.uid, cAm)
							ku_tx_list.append(kc_tax)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)

					# OIL以外(10500 & 10600含む)
					elif SC_Check(iv.s_code.uid) == "nOIL":
						sv, cTax, cAm = nOIL_Cal(iv.s_code.uid, iv.g_code.uid, iv.amount, iv.value, iv.tax, jtax, iv.red_code, iv.m_datetime)
						# nOIL_Cal(sc, gc, am, vl, tax, jtax, red, md):
						# sv, cTax = nOIL_Cal(iv.s_code.uid, iv.value, iv.tax, jtax, iv.red_code)
						# nOIL_Cal(sc,value,tax,jtax,red_code):
						# total_list.append(sv)
						tax_list.append(cTax)

						if iv.value == 0 and iv.s_code.uid == "10500":
							tu_am_list.append(cAm/100)
							# inVl_Cal(sc, gc, am, vl, tax, red, md):
							tu_list.append(sv-cTax)
							ntax_list.append(sv-cTax)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)
						elif iv.s_code.uid == "10500":
							tu_am_list.append(cAm/100)
							tu_list.append(sv-cTax)
							ntax_list.append(sv-cTax)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)
						else:
							ntax_list.append(sv-cTax)
							noil_list.append(sv-cTax)
							if iv.red_code:
								slip_list.append(-1)
							else:
								slip_list.append(1)

					# その他 : 現金 & OIL & OIL以外(10500 & 10600含む)
					else:
						sv = 0

				## Prev Month ##
				for biv in bIVs:
					# 消費税率 : 2019/10/01 => 10%, 2014/4/1 => 8%
					jtax = jTax(biv.m_datetime)

					# OIL
					if SC_Check(biv.s_code.uid) == "OIL":
						sv, cTax, cAm = OIL_Cal(biv.s_code.uid, biv.g_code.uid, biv.amount, biv.value, biv.tax, jtax, biv.red_code, biv.m_datetime)
						bntax_list.append(sv)
						btax_list.append(cTax)

						if biv.s_code.uid == "10200":
							kc_tax = kTax_Cal(biv.s_code.uid, cAm)
							bku_tx_list.append(kc_tax)

					# OIL以外(10500 & 10600含む)
					elif SC_Check(biv.s_code.uid) == "nOIL":
						sv, cTax, cAm = nOIL_Cal(biv.s_code.uid, biv.g_code.uid, biv.amount, biv.value, biv.tax, jtax, biv.red_code, biv.m_datetime)
						btax_list.append(cTax)

						if biv.value == 0 and biv.s_code.uid == "10500":
							bntax_list.append(sv - cTax)
						elif biv.s_code.uid == "10500":
							bntax_list.append(sv - cTax)
						else:
							bntax_list.append(sv-cTax)

					# その他 : 現金 & OIL & OIL以外(10500 & 10600含む)
					else:
						sv = 0

				## Value : Sum ##
				incash_vl = sum(incash_list)
				slip_vl = sum(slip_list)
				ntax_vl = sum(ntax_list)
				tax_vl = sum(tax_list)

				bntax_vl = sum(bntax_list)
				btax_vl = sum(btax_list)
				bku_tx = sum(bku_tx_list)

				high_am = sum(high_am_list)
				high_vl = sum(high_list)
				reg_am = sum(reg_am_list)
				reg_vl = sum(reg_list)
				ku_am = sum(ku_am_list)
				ku_vl = sum(ku_list)
				ku_tx = sum(ku_tx_list)

				tu_am = sum(tu_am_list)
				tu_vl = sum(tu_list)

				no_oil = sum(noil_list)

				total_vl = ntax_vl + tax_vl + ku_tx
				btotal_vl = bntax_vl + btax_vl + bku_tx

				## Value : Context ##
				context['incash_vl'] = incash_vl
				context['slip_vl'] = slip_vl
				context['total_vl'] = total_vl
				context['ntax_vl'] = ntax_vl
				context['tax_vl'] = tax_vl

				context['btotal_vl'] = btotal_vl

				context['high_am'] = high_am
				context['high_vl'] = high_vl
				context['reg_am'] = reg_am
				context['reg_vl'] = reg_vl
				context['ku_am'] = ku_am
				context['ku_vl'] = ku_vl
				context['ku_tx'] = ku_tx

				context['tu_am'] = tu_am
				context['tu_vl'] = tu_vl

				context['no_oil'] = no_oil

			except Exception as e:
				print("Exception - views.py / dl=True / Caluculate  : %s" % e)
			## End of Caluculate ##

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## DB : Setup ##
			names, IVs, bIVs, lastmonths, BFs = DB_vInvoice(self, "", "", "", "")
			# names, IVs, bIVs, lastmonths, BFs = DB_vInvoice(self, "", "")
			# names, IVs, lastmonths, BFs, VLs = DB_vInvoice(self, "", "")

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

		## Paginator : Setup ##
		paginator = Paginator(IVs, 30)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1
		try:
			IVs = paginator.page(page)
		except(EmptyPage, InvalidPage):
			IVs = paginator.page(1)
		context['ivs'] = IVs
		# context['vls'] = VLs

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
