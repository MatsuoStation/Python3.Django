#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.sFreee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.Dj.sFreee.Views.py - Ver.3.93.20 Update:2021.09.30" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from .forms import DateForm
from django.core.paginator import Paginator, EmptyPage, InvalidPage

### Google.API ###
from .Util.Connect_GSpread import connect_gspread
import pandas as pd
import numpy as np
import math
# import seaborn as sns

### MySQL ###
from Finance.models import SHARPnPOS_1501_2107
from datetime import datetime, timedelta
from .Util.deadline import DeadLine
from .Util.db_sFreee import DB_sFreee

### Google Apps Script ###
class GAS(ListView):
	model = SHARPnPOS_1501_2107
	form_class = DateForm
	template_name = 'sFreeeList.html'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		mdate_post = request.POST['mdate']
		if form.is_valid():
			return HttpResponseRedirect('/sFreee/GAS/%s' % mdate_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## GAS : SpreadSheet - Setup ##
		spsh_name = "SS_U"
		ws = connect_gspread(spsh_name)
		ws_list = ws.worksheets()

		## Search : m_datetime ##
		context['form'] = DateForm()
		if self.kwargs.get('mdate'):
			mdate = self.kwargs.get('mdate')
		else:
			mdate = '2000-01'

		## * try: * dl = Ture ##
		try:
			## 期間設定 ##
			dl = mdate + '-01'
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			# dd = dlstr.day  # DeadLine : Day
			dlb, dla = DeadLine(dlstr)

			## DB : Setup ##
			SnPs, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs, SnP20, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs = DB_sFreee(self, dlb, dla)

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## 期間設定 ##
			dl = mdate + '-01'
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			# dd = dlstr.day  # DeadLine : Day
			dlb, dla = DeadLine(dlstr)

			## DB : Setup ##
			SnPs, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs, SnP20, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs = DB_sFreee(self, dlb, dla)

		context['mdate'] = mdate
		context['dlb'] = dlb
		context['dla'] = dla

		## GAS : 初期データ設定 ##
		SnPs_count = len(SnPs)
		context['snps_count'] = SnPs_count
		Pager_count = 50;
		SnPsVs = SnPs

		## Paginator : Setup ##
		paginator = Paginator(SnPs, Pager_count)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1
		try:
			SnPs = paginator.page(page)
		except(EmptyPage, InvalidPage):
			SnPs = paginator.page(1)
		context['snps'] = SnPs

		## GAS : データ設定 ##
		snp_list = list()
		try:
			Pager_Page = SnPs.number
			Pager_LastPage = math.ceil(SnPs_count / Pager_count)
		except Exception as e:
			print("Exception - Pager_page : %s" % e)

		c = 0
		for snpv in SnPs:
		# for snpv in SnPsVs:

			### GAS : 初期設定（ページ数)
			if Pager_Page == 1:
				p = 0
			else:
				p = ((Pager_Page - 1) * 50)

			### GAS : 初期設定（入力データ)
			pName = '=IFERROR(IF(Y' + str(c + 2 + p) + '<>"",VLOOKUP(VLOOKUP(Y' + str(c + 2 + p) + ',IMPORTRANGE("1gFItc1Ta3hXS1Ad6jEUjMfgNdU_y8ozHGuX_tmW1u5Q","PartnersList!D2:E"),2,false),IMPORTRANGE("1gFItc1Ta3hXS1Ad6jEUjMfgNdU_y8ozHGuX_tmW1u5Q","PartnersList!A2:C"),3,false),""))'
			pItem = '=IFERROR(IF(AB' + str(c + 2 + p) + '<>"",VLOOKUP(VLOOKUP(AB' + str(c + 2 + p) + ',IMPORTRANGE("1vBG3-DMn8BANxhboZ2JkdzmNZm-DITy9-UPg9ID5bs8","ItemsList!D2:E"),2,false),IMPORTRANGE("1vBG3-DMn8BANxhboZ2JkdzmNZm-DITy9-UPg9ID5bs8","ItemsList!A2:C"),3,false),""))'
			tax_section = '=IF(A' + str(c + 2 + p) + '<>"",1,0)'

			'''
			if snpv.amount != 0:
				pAm = (snpv.amount / 100)
				oAm = '=IFERROR(IF(AK' + str(c + 2 + p) + '=8,-(' + str(pAm) + '),' + str(pAm) + '))'

				if snpv.value != 0:
					oUnit = (snpv.value / pAm)
					oVl = '=IFERROR(IF(AK' + str(c + 2 + p) + '=8,-(' + str(snpv.value) + '),' + str(snpv.value) + '))'
					oTax = '=IFERROR(IF(AK' + str(c + 2 + p) + '=8,-(' + str(snpv.tax) + '),' + str(snpv.tax) + '))'
				else:
					oUnit = 0
					oVL = 0
					oTax = 0
			else:
				pAm = 0
				oAm = 0
				oUnit = 0
				oVL = 0
				oTax = 0
			'''


			p_r_code = str(snpv.p_code)+'/'+str(snpv.r_code)
			if p_r_code == '10/0' or p_r_code == '10/1' or p_r_code == '20/9': pRcode = '現金'
			else: pRcode = ''

			## GAS : 赤伝先
			if snpv.c_day != 0: oCC = str(snpv.c_day)+'/'+str(snpv.c_no)
			else: oCC = ""


			# oAllCash = '=IFERROR(IF(O'+str(c+2+p)+'="現金",AH'+str(c+2+p)+',""))'

			### GAS : リスト設定
			''' CSV項目 : / 収支区分, 管理番号, 発生日, 決済期日, 取引先, 勘定科目, 税区分, 金額, 税計算区分, 税額, 備考, 品目, 部門, \
				(N) 決済日, 決済口座, 決済金額, Bank.ID, Row, \
				(S) Deal.ID, Pay.ID, W.Type, W.ID, \
				(W) 部門.ID, 取引先ID, g_code, 勘定科目ID, Tax.ID, Item.ID, 未支金額, 決済状況, \
				(AE) 数量, 新単価, 旧単価, 旧金額, 旧税額, 新旧差額, 赤伝 '''
			snp_list.append(['収入', snpv.slip, snpv.m_datetime.strftime('%Y-%m-%d'), '', pName, '売上高', '課税売上8%', 'snpv.value', '内税', 'snpv.tax', oCC, pItem, 'SS関係', \
							 '', pRcode,'', 'BankID', '' , \
							 'DealID', '', '', '', \
							 '', '', snpv.g_code, '', '', snpv.s_code, '', '', \
							 'oAm', '', 'oUnit', 'oVl', 'oTax', '', snpv.red_code])
			c += 1
			# print(c)

		df = pd.DataFrame(snp_list)
		print(df)
		print(str(len(df)))
		print('%s / %s' % (Pager_Page, Pager_LastPage))

		## GAS : シート追加 ##
		newShName = dl[2:-2].replace('-', '')
		ws_list_value = 0

		for i in range(len(ws_list)):
			if ws_list[i].title == newShName:
				ws_list_value = ws_list_value + 1
		ws_list_cpid = ws_list[0].id

		if ws_list_value == 0:
			ws.duplicate_sheet(source_sheet_id=ws_list_cpid, new_sheet_name=newShName, insert_sheet_index=len(ws_list))

		## GAS : 行数追加 ##
		write_ws = ws.worksheet(newShName)
		write_ws.add_rows(Pager_count)
		# write_ws.add_rows(SnPs_count)
		context['write_ws'] = newShName

		## GAS : リスト書き込み　##
		for index, record in df.iterrows():
			cell_list = write_ws.range(index + 2 + p, 1, index + 2 + p, len(record))
			for cell, val in zip(cell_list, record):
				cell.value = val
			write_ws.update_cells(cell_list, value_input_option='USER_ENTERED')
			# write_ws.update_cells(cell_list)

		return context


class GAS_Bak(ListView):
	model = SHARPnPOS_1501_2107
	form_class = DateForm
	# model = Name_Test20
	# form_class = NameForm
	template_name = 'sFreeeList.html'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		mdate_post = request.POST['mdate']
		if form.is_valid():
			return HttpResponseRedirect('/sFreee/GAS/%s' % mdate_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## GAS : SpreadSheet - Setup ##
		spsh_name = "SS_U"
		ws = connect_gspread(spsh_name)
		ws_list = ws.worksheets()

		## Search : m_datetime ##
		context['form'] = DateForm()
		if self.kwargs.get('mdate'):
			mdate = self.kwargs.get('mdate')
		else:
			mdate = '2000-01'

		## * try: * dl = Ture ##
		try:
			## 期間設定 ##
			dl = mdate + '-01'
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			# dd = dlstr.day  # DeadLine : Day
			dlb, dla = DeadLine(dlstr)

			## DB : Setup ##
			SnPs, SnP20, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs = DB_sFreee(self, dlb, dla)

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## 期間設定 ##
			dl = mdate + '-01'
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			# dd = dlstr.day  # DeadLine : Day
			dlb, dla = DeadLine(dlstr)

			## DB : Setup ##
			SnPs, SnP20, SnP30, SnP40, SnP50, SnP90 = DB_sFreee(self, dlb, dla)
			# SnPs = DB_sFreee(self, dlb, dla)

		context['mdate'] = mdate
		context['dlb'] = dlb
		context['dla'] = dla

		## GAS : 初期データ設定 ##
		SnPs_count = len(SnPs)
		context['snps_count'] = SnPs_count
		Pager_count = 50;
		SnPsVs = SnPs

		## Paginator : Setup ##
		paginator = Paginator(SnPs, Pager_count)
		# paginator = Paginator(SnP90, 10)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1
		try:
			SnPs = paginator.page(page)
			# SnP90 = paginator.page(page)
		except(EmptyPage, InvalidPage):
			SnPs = paginator.page(1)
			# SnP90 = paginator.page(1)
		context['snps'] = SnPs
		# context['snps'] = SnP90

		## GAS : データ設定 ##
		snp_list = list()

		try:
			Pager_Page = SnPs.number
			Pager_LastPage = math.ceil(SnPs_count / Pager_count)
		except Exception as e:
			print("Exception - Pager_page : %s" % e)

		for snpv in SnPs:
		# for snpv in SnPsVs:
			''' CSV項目 : / 収支区分, 管理番号, 発生日, 決済期日, 取引先, 勘定科目:Z, 税区分, 金額, 税計算区分, 税額, 備考, 品目, 部門, \
				(N) 決済日, 決済口座, 決済金額, Bank.ID, Row, \
				(S) Deal.ID, Pay.ID, W.Type, W.ID, \
				(W) 部門.ID, 取引先ID, g_code, 勘定科目ID, Tax.ID, Item.ID, 未支金額, 決済状況 '''
			snp_list.append(['収入', snpv.slip, snpv.m_datetime.strftime('%Y-%m-%d'), '', snpv.g_code, '売上高', '', snpv.value, '', snpv.tax, snpv.red_code, snpv.s_code, 'SS関係', \
							 '','','', 'BankID', '' , \
							 'DealID', '', '', '', \
							 '', '', snpv.g_code, '', '', '', '', ''])
			# snp_list.append(['', snpv.slip, snpv.m_datetime.strftime('%Y-%m-%d'), '', snpv.g_code, '', '', snpv.value, '', snpv.tax, 'red_code:' + snpv.red_code, snpv.s_code, '', '', '', ''])
			# m_date = datetime.strptime(snpv.m_datetime, '%Y-%m-%d')
			# mdate_list.append(m_date)

		df = pd.DataFrame(snp_list)
		# df = pd.DataFrame(snp_list, columns=['s_code', 'g_code'])
		# COLMAX = len(df.columns)
		# ROWMAX = len(df.index) + 1
		# print(snp_list)
		print(df)
		print(str(len(df)))
		print('%s / %s' % (Pager_Page, Pager_LastPage))
		# print(Pager_Page)
		# print(Pager_LastPage)

		## GAS : シート追加 ##
		newShName = dl[2:-2].replace('-', '')
		# newShName = dl.replace('20', '').replace('-', '')
		ws_list_value = 0

		for i in range(len(ws_list)):
			# context['ws_list_len'] = len(ws_list)
			# context['ws_list_name'] = ws_list[i].title
			if (ws_list[i].title == newShName):
				ws_list_value = ws_list_value + 1
		ws_list_cpid = ws_list[0].id
		# context['ws_list_cpid'] = ws_list_cpid

		if ws_list_value == 0:
			ws.duplicate_sheet(source_sheet_id=ws_list_cpid, new_sheet_name=newShName, insert_sheet_index=len(ws_list))
			# ws.add_worksheet(title=newShName, rows=100, cols=25)
		# context['ws_list_vl'] = ws_list_value

		## GAS : 行数追加 ##
		# write_ws = ws.get_worksheets(newShName)
		write_ws = ws.worksheet(newShName)
		write_ws.add_rows(SnPs_count)
		# write_ws = ws.get_worksheet(len(ws_list)-1)
		# ws_list[0].update_cell(1, 3, cell_value)
		context['write_ws'] = newShName

		## GAS : リスト書き込み　##
		if Pager_Page == 1:
			p = 0
		else:
			p = ((Pager_Page - 1) * 50)

		for index, record in df.iterrows():
			cell_list = write_ws.range(index + 2 + p, 1, index + 2 + p, len(record))
			# cell_list = write_ws.range('C3:G' + str(len(df)+2))

			for cell, val in zip(cell_list, record):
				cell.value = val
			write_ws.update_cells(cell_list)

		# (Def.OK) write_ws.update([df.columns.values.tolist()] + df.values.tolist())
		# (OK) write_ws.update('E3:F12', snp_list)
		# (OK) write_ws.append_row(snp_list)

		return context


def GAS_Def(request):
	## GAS : SpreadSheet - Setup ##
	spsh_name = "SS_U"
	# spsh_name = "GooglePython"

	ws = connect_gspread(spsh_name)
	# ws = connect_gspread(gJsonFile, spsh_name)
	ws_list = ws.worksheets()

	## GAS : Read ##
	cell_value = ws_list[0].acell('A1').value

	## GAS : Write ##
	ws_list[0].update_cell(1, 18, cell_value)

	return HttpResponse("A1 = %s" % cell_value)
	# return HttpResponse("SS_U.Json.File = %s : %s" % (len(ws_list), ws_list[0].title))
	# return HttpResponse("Google.Json.File = %s : %s , %s" % (len(ws_list), ws_list[0].title, ws_list[1].title))
	# return HttpResponse("Hello sFreee/GAS/ You're at the Google Apps Script.")

### Default ###
def index(request):
	return HttpResponse("Hello RDS to CSV sFreee/Index.py. You're at the Index.")
