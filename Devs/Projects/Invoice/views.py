#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Invoice.Views.py - Ver.3.8.5 Update:2018.04.22" |
#//+------------------------------------------------------------------+
#//|                                                            @dgel |
#//|                     https://stackoverflow.com/questions/12518517 |
#//|               /request-post-getsth-vs-request-poststh-difference |
#//+------------------------------------------------------------------+
#//|                                                       @yoheiMune |
#//|                       https://www.yoheim.net/blog.php?q=20160409 |
#//+------------------------------------------------------------------+
### MatsuoStation.Com ###
# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.urls import reverse

from django.views.generic import ListView
from Finance.models import Name_Test, Items_Test, SHARP_Test, Value_Test
from .forms import NameForm
# from .forms import NameForm, MyForm
from Finance.models import Name_Test02, SHARP_Test02

from Finance.models import Invoice_Test10, Name_Test10, Items_Test10, Value_Test10
from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20, Value_Test20

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

from django.utils import dateformat
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Count, Min, Max, Sum, Avg


class Invoice_List(ListView):

	model = Name_Test20
	# model = SHARP_Test
	form_class = NameForm
	template_name = 'list.html'
	# (OK) context_object_name = "sharptb"
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		# deadline_post = request.POST['deadline']
		if form.is_valid():
			# (OK)return HttpResponseRedirect('/Invoice/%s/?dl=%s' % (nid_post, deadline_post) )
			return HttpResponseRedirect( '/Invoice/%s' % nid_post )
			# return HttpResponseRedirect( '/Invoice/%s' % nid_post, kwargs={'dl':deadline_post} )
			# return redirect(request, '/Invoice/%s' % nid_post, kwargs={'deadline':deadline_post} )
			# return render(request, '/Invoice/%s' % nid_post, {'deadline': deadline_post})
			# (Test) return HttpResponseRedirect('/Invoice/%s' % lastday_post)

		return render(request, self.template_name, {'form': form})

	'''
	def h_name(self):
		sharps = SHARP_Test.objects.filter(g_code__endswith=self.kwargs.get('nid'))

		for sharp in sharps:
			h_name = Items_Test.objects.all().filter(uid__startswith=sharp.s_code)
		return h_name
	'''

	# def get_queryset(self):
		# uid = self.request.GET.get('uid')
		# uid = self.request.POST.get('uid')

		# (OK) return SHARP_Test.objects.filter(g_code__endswith=self.kwargs.get('nid'))
		# return NAME_Test.objects.filter(uid__endswith=self.kwargs.get('nid'))
		# return SHARP_Test.objects.filter(g_code__endswith=uid)
		# return SHARP_Test.objects.filter(g_code="0104")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = NameForm()

		context['gid'] = self.kwargs.get('nid')

		# (Def.OK) context['deadlines'] = '2018-04-05'
		# context['deadlines'] = datetime(self.kwargs.get('deadline'),'Y-m-d')
		# context['deadlines'] = self.kwargs.get('deadline')
		# context['deadlines'] = self.request.POST.get('deadline', 'None')
		# (GET.OK) context['deadlines'] = self.request.GET.get('dl', '0000-00-00')


		# dl = self.request.GET.get('dl', '')
		# if dl:

		dd_list = list()

		try:
			dl = self.request.GET.get('dl', '')
			# (Def.OK) dld = datetime.strptime(dl, '%Y-%m-%d')
			dlt = datetime.strptime(dl, '%Y-%m-%d')
			# (OK) dld = dlt + timedelta(days=1)

			dd = dlt.day
			if dd == 20 or dd == 25:
				dld = dlt + timedelta(days=1) - relativedelta(months=1)
				dlm = dlt + timedelta(days=1) - timedelta(microseconds=1)
				# dld = dlt - relativedelta(months=1) + timedelta(days=1)
				# dlm = dld + relativedelta(months=2) - timedelta(microseconds=1)

			else:
				dt = dlt - relativedelta(months=1)
				dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
				dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)


			# dt = dlt - relativedelta(months=1)
			# dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
			# (OK) dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)
			# dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)
			# dlm = dlt + relativedelta(months=1) - timedelta(microseconds=1)
			# dld = dl + timedelta(days=dl.day+1)
			# dld = dl.strptime(dl, '%Y-%m-%d') + timedelta(days=dl.strptime(dl, '%Y-%m-%d')+1)
			# dld = dl + timedelta(days=+1)

			# (car_code to m_datetime)
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			# (Def.Order.Date) IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code',)
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
			# months = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct()
			# months = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct()
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

			# check_days = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')

			context['dlms'] = dlms

			### Income Total Cash ###
			incash_list = list()
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values


			### Total Value Cash ###
			total_list = list()
			notax_list = list()
			tax_list = list()

			toyu_a_list = list()
			toyu_list = list()

			keiyu_a_list = list()
			keiyu_list = list()
			ktax_list = list()

			high_a_list = list()
			high_list = list()

			reg_a_list = list()
			reg_list = list()

			nonoil_list = list()
			ndigits = 0
			jtax = 0.08

			try:
				for iv in IVs:
					### 現金関係 & 振込関係
					if iv.s_code.uid == "00000":
						sv = 0
						total_list.append(sv)
					elif iv.s_code.uid == "00002":
						sv = 0
						total_list.append(sv)

					### 金額 : True
					elif iv.value:
						### 単価 : True
						if iv.unit != 0:
							notax_v = iv.value
							tax_v = iv.tax
							sv = notax_v + tax_v

							if iv.red_code:
								notax_v = -(notax_v)
								tax_v = -(tax_v)
								sv = -(sv)

							total_list.append(sv)
							notax_list.append(notax_v)
							tax_list.append(tax_v)

							if iv.s_code.uid == "10500":
								t_amount = iv.amount/100

								if iv.red_code:
									t_amount = -(t_amount)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

						### 単価 : False
						else:
							### 税金 : True
							if iv.tax != 0:
								tax_v = iv.tax
								notax_v = iv.value
								sv = notax_v + tax_v

								if iv.red_code:
									tax_v = -(tax_v)
									notax_v = -(notax_v)
									sv = -(sv)

								total_list.append(sv)
								notax_list.append(notax_v)
								tax_list.append(tax_v)

								if iv.s_code.uid == "10500":
									t_amount = iv.amount/100

									if iv.red_code:
										t_amount = -(t_amount)

									toyu_a_list.append(t_amount)
									toyu_list.append(notax_v)

							### 税金 : False
							else:
								# values = iv.value - (iv.value / 1.08)
								values = iv.value - (iv.value / (1+jtax))
								d_point = len(str(values).split('.')[1])
								if ndigits >= d_point:
									tax_v = int(round(values, 0))
								c = (10 ** d_point) * 2
								tax_v = int(round((values * c + 1) / c, 0))
								sv = iv.value
								notax_v = sv - tax_v

								if iv.red_code:
									tax_v = -(tax_v)
									sv = -(sv)
									notax_v = -(notax_v)

								tax_list.append(tax_v)
								notax_list.append(notax_v)
								total_list.append(sv)

								if iv.s_code.uid == "10500":
									t_amount = iv.amount/100

									if iv.red_code:
										t_amount = -(t_amount)

									toyu_a_list.append(t_amount)
									toyu_list.append(notax_v)

					### 金額 : False
					elif Value_Test20.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, m_datetime__lte=iv.m_datetime):
						v_values = Value_Test20.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, m_datetime__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								ks_values = (v.value - 32.1) * k_amount
								d_point = len(str(ks_values).split('.')[1])
								if ndigits >= d_point:
									ks_value = round(ks_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ks_values * c + 1) / c, 0))

								k_tax = -(-32.1 * iv.amount / 100)
								k_tax = int(k_tax)

								# ks_tax = notax_v * 0.08
								ks_tax = notax_v * jtax
								dd_point = len(str(ks_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ks_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ks_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v + k_tax

								if iv.red_code:
									notax_v = -(notax_v)
									k_amount = -(k_amount)
									k_tax = -(k_tax)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								keiyu_a_list.append(k_amount)
								keiyu_list.append(notax_v)
								ktax_list.append(k_tax)

						# ハイオク = "10000"
						elif iv.s_code.uid == "10000":
							for v in v_values:
								h_amount = iv.amount / 100
								hs_values = v.value * h_amount
								d_point = len(str(hs_values).split('.')[1])
								if ndigits >= d_point:
									hs_value = round(hs_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((hs_values * c + 1) / c, 0))

								# hs_tax = notax_v * 0.08
								hs_tax = notax_v * jtax
								dd_point = len(str(hs_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(hs_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((hs_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v

								if iv.red_code:
									h_amount = -(h_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								high_a_list.append(h_amount)
								high_list.append(notax_v)

						# レギュラー = "10100"
						elif iv.s_code.uid == "10100":
							for v in v_values:
								r_amount = iv.amount / 100
								rs_values = v.value * r_amount
								d_point = len(str(rs_values).split('.')[1])
								if ndigits >= d_point:
									rs_value = round(rs_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((rs_values * c + 1) / c, 0))

								# hs_tax = notax_v * 0.08
								rs_tax = notax_v * jtax
								dd_point = len(str(rs_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(rs_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((rs_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v

								if iv.red_code:
									r_amount = -(r_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								reg_a_list.append(r_amount)
								reg_list.append(notax_v)



					elif Value_Test20.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date01__lte=iv.m_datetime):
						v_values = Value_Test20.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date01__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								ks_values = (v.value01 - 32.1) * k_amount
								d_point = len(str(ks_values).split('.')[1])
								if ndigits >= d_point:
									ks_value = round(ks_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ks_values * c + 1) / c, 0))

								k_tax = -(-32.1 * iv.amount / 100)
								k_tax = int(k_tax)

								# ks_tax = notax_v * 0.08
								ks_tax = notax_v * jtax
								dd_point = len(str(ks_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ks_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ks_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v + k_tax

								if iv.red_code:
									notax_v = -(notax_v)
									k_amount = -(k_amount)
									k_tax = -(k_tax)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								keiyu_a_list.append(k_amount)
								keiyu_list.append(notax_v)
								ktax_list.append(k_tax)

						# ハイオク = "10000"
						elif iv.s_code.uid == "10000":
							for v in v_values:
								h_amount = iv.amount / 100
								hs_values = v.value01 * h_amount
								d_point = len(str(hs_values).split('.')[1])
								if ndigits >= d_point:
									hs_value = round(hs_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((hs_values * c + 1) / c, 0))

								# hs_tax = notax_v * 0.08
								hs_tax = notax_v * jtax
								dd_point = len(str(hs_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(hs_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((hs_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v

								if iv.red_code:
									h_amount = -(h_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								high_a_list.append(h_amount)
								high_list.append(notax_v)

						# レギュラー = "10100"
						elif iv.s_code.uid == "10100":
							for v in v_values:
								r_amount = iv.amount / 100
								rs_values = v.value01 * r_amount
								d_point = len(str(rs_values).split('.')[1])
								if ndigits >= d_point:
									rs_value = round(rs_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((rs_values * c + 1) / c, 0))

								# hs_tax = notax_v * 0.08
								rs_tax = notax_v * jtax
								dd_point = len(str(rs_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(rs_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((rs_tax * cc + 1) / cc, 0))

								sv = notax_v + tax_v

								if iv.red_code:
									r_amount = -(r_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								reg_a_list.append(r_amount)
								reg_list.append(notax_v)

					else:
						sv = 0
						total_list.append(sv)

				total_values = sum(total_list)
				notax_values = sum(notax_list)
				tax_values = sum(tax_list)

				toyu_amounts = sum(toyu_a_list)
				toyu_values = sum(toyu_list)

				keiyu_amounts = sum(keiyu_a_list)
				keiyu_values = sum(keiyu_list)
				ktax_values = sum(ktax_list)

				high_amounts = sum(high_a_list)
				high_values = sum(high_list)

				reg_amounts = sum(reg_a_list)
				reg_values = sum(reg_list)

				nonoil_values = notax_values - toyu_values - high_values - reg_values - keiyu_values

				context['total_values'] = total_values
				context['notax_values'] = notax_values
				context['tax_values'] = tax_values

				context['toyu_amounts'] = toyu_amounts
				context['toyu_values'] = toyu_values

				context['keiyu_amounts'] = keiyu_amounts
				context['keiyu_values'] = keiyu_values
				context['ktax_values'] = ktax_values

				context['high_amounts'] = high_amounts
				context['high_values'] = high_values

				context['reg_amounts'] = reg_amounts
				context['reg_values'] = reg_values

				context['nonoil_values'] = nonoil_values


			except Exception as e:
				print(e, 'Invoice/views.total_values - in_dl : error occured')

			### LastDay : Check ###
			try:
				if Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid')):
					d_values = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))


				for dmm in dlms:
					dd = dmm.day
					# dd_list.append(dd)
					for d in d_values:
						dv = d.check_day

						if dv == 25:
							if dd >=25:
								dls = (dmm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dmm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						elif dv == 20:
							if dd >= 20:
								dls = (dmm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dmm - timedelta(days=dd-1)) + timedelta(days=dv-1)

						# if dv != 0:
						#	if dd >= 25:
						#		dls = (dmm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
						#	elif dd >=20:
						#		dls = (dmm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
						#	else:
						#		dls = dmm - timedelta(days=dd) + timedelta(days=dv)

						else:
							dls = (dmm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

							'''
							if dd >= dv:	# 31 >= 25
								dls = (dlm + relativedelta(months=1)) - timedelta(days=dd) + timedelta(days=dv)

							elif dd < dv:	# 16 < 25
								dls = dlm - timedelta(days=dd) + timedelta(days=dv)

							else:
								dls = dlm + relativedelta(months=1) - timedelta(days=dd)

						else:
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)
						'''

						dd_list.append(dls)

						dds = sorted(set(dd_list), key=dd_list.index)

						# context['dd'] = dd_list
						context['dds'] = dds

			except Exception as e:
				print(e, 'Invoice/views.py_dds : error occured')


			context['deadlines'] = dl

			dlb = dlt + timedelta(days=1) - relativedelta(months=1)
			context['dlb'] = dlb
			dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
			context['dla'] = dla


			# for dlm in dlms:
			#	context['deadlines'] = dlm.strftime('%Y-%m')

			# context['deadlines'] = months.dates('m_datetime', 'month', order='DESC')
			# for mt in months:
				# context['deadlines'] = mt.strftime('%Y-%m')
				# context['deadlines'] = months

				# context['deadlines'] = dl

		# else: dl = ''
		except Exception as e:
			# dl = self.request.GET.get('dl', '')
			# dld = dl.strptime(dl, '%Y-%m-%d')

			# (car_code to m_datetime)
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			# (Def.Order.Date) IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			### Income Total Cash ###
			'''
			incash_list = list()
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values
			'''

			# dd_list = list()

			### LastDay : Check ###
			try:
				if Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid')):
					d_values = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))


				for dlm in dlms:
					dd = dlm.day
					# dd_list.append(dd)
					for d in d_values:
						dv = d.check_day

						if dv == 25:
							if dd >=25:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						elif dv == 20:
							if dd >= 20:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)


						# if dv != 0:
						#	if dd >= 25:
						#		dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
						#	elif dd >=20:
						#		dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv) - timedelta(days=1)
						#	else:
						#		dls = dlm - timedelta(days=dd) + timedelta(days=dv)


						# if dv != 0:
						#	if dd >= dv:	# 31 >= 25

						#		dls = (dlm + relativedelta(months=1)) - timedelta(days=dd) + timedelta(days=dv)

						#	elif dd < dv:	# 16 < 25
						#		dls = dlm - timedelta(days=dd) + timedelta(days=dv)

						#	else:
						#		dls = dlm + relativedelta(months=1) - timedelta(days=dd)

						else:
							# dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

						dd_list.append(dls)

						dds = sorted(set(dd_list), key=dd_list.index)

						# context['dd'] = dd_list
						context['dds'] = dds

			except Exception as e:
				print(e, 'Invoice/views.py_dds : error occured')

			context['deadlines'] = dl

			print(e, 'Invoice/Views : error occured')


		# deadline = datetime.format(self.kwargs.get('deadline'), 'Y-m-d')
		'''
		deadline = []
		if deadline:
			IVs = Invoice_Test20.objects.filter( g_code__uid=self.kwargs.get('nid'), m_datetime__gte='2018-03-31' ).select_related('g_code').select_related('s_code').order_by('car_code')
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

		else:
			# IVs = Invoice_Test20.objects.filter( g_code__uid=self.kwargs.get('nid'), m_datetime__gte='2018-02-28', m_datetime__lt='2018-04-01' ).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
			# (Def.OK) IVs = Invoice_Test20.objects.filter( g_code__uid=self.kwargs.get('nid'), m_datetime__gte='2018-03-31' ).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
			IVs = Invoice_Test20.objects.filter( g_code__uid=self.kwargs.get('nid') ).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

		'''
		# context['nid_post'] = request.POST.get('nid')

		# context['nid'] = request.POST['nid']
		# context['post_nid'] = self.NameForm

		# sharps = SHARP_Test02.objects.filter(g_code__uid__endswith='0104')
		# sharps = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid'))
		# (Ver.3.7.3.OK) sharps = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')
		# (Ver.3.7.7.OK) IVs = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code').select_related('s_code')
		# (Ver.3.7.14.OK) IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code')
		# IVs = Invoice_Test10.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code')
		# names = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# (Ver.3.7.7.OK) names = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')
		# (Ver.3.7.14.OK) names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
		# (Ver.3.7.7.OK) items = Invoice_Test10.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('s_code')
		# items = Invoice_Test20.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('s_code')
		# values = Value_Test10.objects.all().filter(uid="0104", s_code="10100")
		# (Ver.3.7.7.OK) values = Value_Test10.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code="10100")
		# values = Value_Test20.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code="10100")

		for name in names:
			context['names'] = name.g_code.name
		# for name in IVs:
		#	context['names'] = name.g_code.name

		# for item in items:
		#	context['items'] = item.s_code.h_name
		# context['values'] = values

		# for i in IVs:
		#	values = Value_Test10.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code=i.s_code)

		#	for v in values:
		#		context['values'] = v.value


		# for v in values:
		#	context['values'] = v.value

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


		'''
		sharps = SHARP_Test.objects.all().filter(
			g_code__endswith=self.kwargs.get('nid'),
		)
		'''

		# (Ver.3.7.3.OK) names = SHARP_Test02.objects.filter(g_code__uid__endswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# names = SHARP_Test02.objects.filter(g_code__uid__startswith=self.kwargs.get('nid')).select_related('g_code')[:1]
		# (OK) names = Name_Test02.objects.filter(uid__endswith=self.kwargs.get('nid'))
		# (OK) names = Name_Test.objects.all().filter(uid__endswith=self.kwargs.get('nid'))
		# names = Name_Test.objects.all().filter(uid__startswith="0104")

		# items = Items_Test.objects.all().filter(uid__startswith='1010')
		# items = Items_Test.objects.all().filter(uid__startswith="1020")

		# context['sharps'] = sharps
		# context['names'] = names
		# (Ver.3.7.3.OK) for name in names:
			# context['names'] = name.name
		# (Ver.3.7.3.OK) 	context['names'] = name.g_code.name


		# context['names'] = names

		# items = Items_Test.objects.filter(uid=sharps.objects.filter(s_code))
		# context['items'] = i.h_name

		# (Ver.3.7.3.OK) for sharp in sharps:
			# items = Items_Test.objects.all().filter(uid__startswith='1010')
			# items = Items_Test.objects.all().filter(uid__startswith='10200')
		# (Ver.3.7.3.OK) 	items = Items_Test.objects.filter(uid=sharp.s_code)
		# (Ver.3.7.3.OK) 	for i in items:
		# (Ver.3.7.3.OK) 		context['items'] = i.h_name

		# (Ver.3.7.3.OK) context['sharps'] = sharps
		# context['items'] = items

		#context['h_name'] = self.h_name

		# items = Items_Test.objects.all().filter(uid__startswith="1010")
		# context['s_codes'] = items

		# context['sc'] = Items_Test.objects.filter(uid__startswith="1010")

		return context


def index(request):
	# return HttpResponse("Invoice Page!! Welcome to Devs.MatsuoStation.Com!")

	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/Invoice/%s' % nid_post)

	else:
		form = NameForm()

	return render(request, 'invoice.html', {'form': form})

	# items = Items_Test.objects.all().order_by('uid')
	# names = Name_Test.objects.all().order_by('uid')
	# return render(request, 'invoice.html',
	#	{
	#		# 'names' : Name_Test.objects.all(),
	#		# 'Yuki'	: 'Yuki',
	#		'names' : names,
	#		'items'	: items,
	#	}
	# )


def form_invoice(request, nid):
	# return HttpResponse("You're looking at Form_Invoice %s" % uid)
	forms = get_object_or_404(Name_Test, uid__endswith=nid)
	# forms = get_list_or_404(Name_Test, uid=nid)
	sharps = SHARP_Test.objects.all().filter(g_code__endswith=nid)
	items = Items_Test.objects.all()


	if request.method == 'POST':
		form = NameForm(request.POST)

		if form.is_valid():
			pass

	else:
		form = NameForm()

	return render(request, 'form.html',
		{
			'form'	: form,
			'forms'	: forms,
			'sharps': sharps,
			'items'	: items,
		}
	)


def form_name(request):
	names = Name_Test.objects.all().order_by('uid')

	if request.method == 'POST':
		form = NameForm(request.POST)

		if form.is_valid():
			pass

	else:
		form = NameForm()

	return render(request, 'form.html',
		{
			'names'	: names,
			'form'	: form,
		}
	)

''' (Def)
def form_test(request):
	if request.method == "POST" :
		form = MyForm(data=request.POST)	# 受け取ったPOSTデータを渡す
		if form.is_valid():					# 受け取ったデータの正当性確認
			pass							# 正しいデータを受け取った場合の処理
	else:
		form = MyForm()

	# form = MyForm()

	return render(request, 'form.html',
		{
			'form'	: form,
		}
	)
'''