#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.sFreee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.Dj.sFreee.Views.py - Ver.3.93.11 Update:2021.09.29" |
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
		for index, record in df.iterrows():
			cell_list = write_ws.range(index + 2, 1, index + 2, len(record))
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
