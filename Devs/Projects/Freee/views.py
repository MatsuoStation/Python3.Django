#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Freee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.65 Update:2019.10.02" |
#//|               https://qiita.com/hujuu/items/b0339404b8b0460087f9 |
#//|                https://qiita.com/mazu/items/77db19ca2caf128cc062 |
#//|                            https://techacademy.jp/magazine/18994 |
#//+------------------------------------------------------------------+
#//|                                     * Scraping : BeautifulSoup * |
#//|                                                           @hujuu |
#//|               https://qiita.com/hujuu/items/b0339404b8b0460087f9 |
#//|                                                       @tomson784 |
#//|           https://qiita.com/tomson784/items/88a3fd2398a41932762a |
#//+------------------------------------------------------------------+
#//|                                           * Regular Expression * |
#//|                                https://www.sejuku.net/blog/23232 |
#//+------------------------------------------------------------------+
#//|                                                       * IsFile * |
#//|                            https://techacademy.jp/magazine/18994 |
#//+------------------------------------------------------------------+
#//|                                                       * Pandas * |
#//|                 https://note.nkmk.me/python-pandas-read-csv-tsv/ |
#//|                 https://note.nkmk.me/python-pandas-dtype-astype/ |
#//| https://www.soudegesu.com/post/python/pandas-preprocess-columns/ |
#//|                                                        @haru1977 |
#//|            https://qiita.com/haru1977/items/53c582eb9e264ccf8574 |
#//|                                                           @ysdyt |
#//|               https://qiita.com/ysdyt/items/9ccca82fc5b504e7913a |
#//|                                              * Pandas : Delete * |
#//|          https://linus-mk.hatenablog.com/entry/2019/01/10/003349 |
#//|                        https://note.nkmk.me/python-pandas-query/ |
#//|                     https://pythondatascience.plavox.info/pandas |
#//|          /%E8%A1%8C%E3%83%BB%E5%88%97%E3%82%92%E5%89%8A%E9%99%A4 |
#//|                                    * Pandas : read_cse.usecols * |
#//|   http://starpentagon.net/analytics/python_csv_specific_columns/ |
#//|                                          * Pandas : for x in a * |
#//|                    https://ja.stackoverflow.com/questions/47331/ |
#//+------------------------------------------------------------------+
#//|                                                        * toCSV * |
#//|                    https://blog.imind.jp/entry/2019/04/12/224942 |
#//+------------------------------------------------------------------+
#//|                                             * Decimal.quantize * |
#//|              https://note.nkmk.me/python-round-decimal-quantize/ |
#//+------------------------------------------------------------------+
# rom django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import HttpResponse

from django.views.generic import ListView
from Finance.models import Name_Test20
from .forms import YearForm

import pymysql.cursors

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

import requests, re, time, os

import pandas as pd
import numpy as np

from datetime import datetime, date
from decimal import (Decimal, ROUND_DOWN, ROUND_HALF_UP)

jtax8 = 0.08
ndigits = 0

### DictFetchAll ###
def dictfetchall(cursor):
	# "Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

### CSV.Write ###
def CSV_Write(file, LastPage, url):

	wr = csv.writer(file)

	for page in range(1, LastPage+1):

		## URL.ReSetup
		urlPage = url + "?page=" + str(page)
		time.sleep(1)
		htmlPage = urlopen(urlPage)
		bsObjPage = BeautifulSoup(htmlPage, "html.parser")

		## Table
		table = bsObjPage.findAll("table", {"class":"table"})[0]

		if page == 1:
			rows = table.findAll("tr")

		else:
			rows = table.findAll("tr")[1:]

		for row in rows:
			csvRow = []
			for cell in row.findAll(['td', 'th']):
				csvRow.append(cell.get_text())
			wr.writerow(csvRow)

### CSV.RedCord ###
def CSV_RedCord(yid):

	### Pandas : ALL_K_*.CSV - 読み取り ###
	df = pd.read_csv("SHARP/K/ALL_K_" + str(yid) + ".csv", sep=',', dtype={'管理番号':'object','CNo':'object'}, index_col=0, encoding='utf-8')

	## カラム : 型設定
	df['管理番号'].astype('str').str.zfill(4)
	df['CNo'].astype('str').str.zfill(4)

	## 抽出
	df_rc = df[df['red'] == 8]

	## toCSV
	df_rc.to_csv("SHARP/K/ALL_RedCode_" + str(yid) + ".csv", encoding='utf-8')

	## df.型出力
	print(df.dtypes)

	return df_rc

### CSV.ALL_Cday_True ###
def CSV_ALL_CDay_True(yid):
	### Pandas : ALL_K_*.CSV - 読み取り
	df_k = pd.read_csv("SHARP/K/ALL_K_" + str(yid) + ".csv", sep=',', dtype={'管理番号':'object','CNo':'object','取引先':'object','決済金額':'object'}, encoding='utf-8')

	### Pandas : ALL_RedCode_*.CSV - 読み取り
	df_r = pd.read_csv("SHARP/K/ALL_RedCode_" + str(yid) + ".csv", sep=',', usecols=['管理番号','発生日','品目','CDay','CNo'], dtype={'管理番号':'object','取引先':'object','CNo':'object','決済金額':'object'}, encoding='utf-8')

	### Pandas : 条件指定
	## ALL :
	# ALL_RedCode_*.CSV : ALL - 行数
	df_r_all_list_len = len(df_r)
	# (OK) context['df_r_all_list_len'] = df_r_all_list_len

	## C_Day : True
	## Target :
	# Target : ALL_RedCode_*.CSV : 対象リスト(Target_List) - 抽出
	df_r_ct_target = df_r.query('CDay.astype("str").str.contains("201")', engine='python')
	# context['df_r_ct_target'] = df_r_ct_target

	# Target : ALL_RedCode_*.CSV : 対象リスト(Target_List) - 行数
	df_r_ct_target_l = len(df_r_ct_target)
	# (OK) context['df_r_ct_target_len'] = df_r_ct_target_l

	# Target : ALL_RedCode_*.CSV : 対象リスト(Target_List) - 削除Index
	df_r_ct_target_v = df_r_ct_target.values.tolist()

	df_r_ct_target_i = []
	for x in df_r_ct_target_v:
		df_r_ct_target_i.append(df_k.reset_index().query('発生日==@x[3] & 管理番号==@x[4] & 品目==@x[2]').index[0])
	#	df_r_ct_target_i.append(df_k.reset_index().query('発生日==@x[1] & 管理番号==@x[2] & 品目==@x[2]').index[0])
	# (OK) context['df_r_ct_target_i'] = df_r_ct_target_i
	# (T.OK) return df_r_ct_target_i


	## Mine :
	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List)) - 抽出
	df_r_ct_mine = df_k[df_k['CDay'].astype('str').str.contains("201")]

	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List) - 行数
	df_r_ct_mine_l = len(df_r_ct_mine)
	# (OK) context['df_r_ct_mine_len'] = df_r_ct_mine_l

	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List) - 削除Index
	df_r_ct_mine_i = df_k[df_k['CDay'].astype('str').str.contains("201")].index.values
	# df_r_ct_mine_i = df_k[df_k['CDay'].astype('str').str.contains("201")].index
	# (OK) context['df_r_ct_mine_i'] = df_r_ct_mine_i
	# (T.OK) return df_r_ct_mine_i

	## Target & Mine : Delete後 - CSV.出力
	## List - Marge
	df_r_ct_i = []
	df_r_ct_i.extend(df_r_ct_target_i)
	df_r_ct_i.extend(df_r_ct_mine_i)
	df_r_ct_i.sort()
	# (T.OK) return df_r_ct_i

	df_r_ct_a = df_k.drop(df_r_ct_i)
	df_r_ct_a.to_csv("SHARP/K/ALL_CT_Del_" + str(yid) + ".csv", encoding='utf-8', index=0)
	# df_r_ct_t = df_k.drop(df_r_ct_target_i)
	# df_r_ct_m = df_r_ct_t.drop(df_r_ct_mine_i)
	# df_r_ct_m.to_csv("SHARP/K/ALL_CT_Del_" + str(yid) + ".csv", encoding='utf-8', index=0)

### CSV.Value30.PULL ###
def CSV_Value_Pull(yid):
	## Value_Test30 : CSV.読み取り
	df_cv = pd.read_csv("Guest/OLD_guestlist/Value_" + str(yid) + ".csv", sep=',', dtype={'s_code':'object'}, \
		header=None, \
		names=["id", "uid", "name", "lpg_code", "tax_code", "s_code", \
		"m_datetime", "value", \
		"date01", "value01", "date02", "value02", "date03", "value03", "date04", "value04", "date05", "value05", \
		"date06", "value06", "date07", "value07", "date08", "value08", "date09", "value09", "date10", "value10", \
		"date11", "value11", "date12", "value12", "date13", "value13", "date14", "value14", "date15", "value15", \
		"date16", "value16", "date17", "value17", "date18", "value18", "date19", "value19", "date20", "value20", \
		"date21", "value21", "date22", "value22", "date23", "value23", "date24", "value24", "date25", "value25", \
		"date26", "value26", "date27", "value27"], encoding='utf-8')

	## 掛売上リスト : ALL_CT_Del_*.CSV - 読み取り
	df_c = pd.read_csv("SHARP/K/ALL_CT_Del_" + str(yid) + ".csv",\
		sep=',',\
		dtype={'取引先':'int', '品目':'object'},\
		# usecols=['発生日','取引先','金額','税額','品目','rcode','amount'],\
		encoding='utf-8')


	'''
	# (Main)
	df_c_9 = df_c.query('rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10000") | \
		rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10100") | \
		rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10200") | \
		rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10500")', engine='python')
	'''
	# (Test)
	df_c_9 = df_c.query('rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10000") | \
		rcode.astype("str").str.contains("9") & 品目.astype("str").str.contains("10500")', engine='python')

	df_c_9_list = df_c_9.values.tolist()
	# '''

	df_c_9_v = []

	try:
		for x in df_c_9_list:
			if len(df_cv.query('uid==@x[4] & s_code==@x[11] & m_datetime<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & m_datetime<=@x[2]').value.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date01<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date01<=@x[2]').value01.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date02<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date02<=@x[2]').value02.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date03<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date03<=@x[2]').value03.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date04<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date04<=@x[2]').value04.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date05<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date05<=@x[2]').value05.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date06<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date06<=@x[2]').value06.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date07<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date07<=@x[2]').value07.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date08<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date08<=@x[2]').value08.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date09<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date09<=@x[2]').value09.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date10<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date10<=@x[2]').value10.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date11<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date11<=@x[2]').value11.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date12<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date12<=@x[2]').value12.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date13<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date13<=@x[2]').value13.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date14<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date14<=@x[2]').value14.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date15<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date15<=@x[2]').value15.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date16<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date16<=@x[2]').value16.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date17<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date17<=@x[2]').value17.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date18<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date18<=@x[2]').value18.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date19<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date19<=@x[2]').value19.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date20<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date20<=@x[2]').value20.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date21<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date21<=@x[2]').value21.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date22<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date22<=@x[2]').value22.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date23<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date23<=@x[2]').value23.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date24<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date24<=@x[2]').value24.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date25<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date25<=@x[2]').value25.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date26<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date26<=@x[2]').value26.values)
			elif len(df_cv.query('uid==@x[4] & s_code==@x[11] & date27<=@x[2]'))!=0:
				df_c_9_v.append(df_cv.reset_index().query('uid==@x[4] & s_code==@x[11] & date27<=@x[2]').value27.values)
			else:
				df_c_9_v.append(0)
				# df_c_9_v.append("100:%s" % x[1] + "-%s" % x[4] + "-%s" % x[0])


	except Exception as e:
		print(e, 'DF_C.9.Value - Freee/Views.dds : error occured.')

	return df_c_9, df_c_9_v


### in_tax : 内税 ###
def in_tax(value):
	values = value - (value / (1+jtax8))

	d_point = len(str(values).split('.')[1])
	ndigits = 0
	if ndigits >= d_point:
		return round(values, 0)
	c = (10 ** d_point) * 2

	return round((values * c + 1) / c, 0)


### out_tax : 外税 ###
def out_tax(value):
	values = value * jtax8

	d_point = len(str(values).split('.')[1])
	ndigits = 0
	if ndigits >= d_point:
		return round(values, 0)
	c = (10 ** d_point) * 2

	return round((values * c + 1) / c, 0)


### Uriage_CSV ###
class Uriage_CSV(ListView):

	model = Name_Test20
	form_class = YearForm
	template_name = 'uriage_csv.html'
	context_object_name = "nametb"

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		yid_post = request.POST['yid']

		if form.is_valid():
			return HttpResponseRedirect( '/Freee/Uriage_CSV/%s' % yid_post )

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = YearForm()

		yid = self.kwargs.get('yid')
		SHARP20_K = 'SHARP20_K_' + str(yid)
		context['SHARP20_K'] = SHARP20_K

		### Scraping : Start ###
		url = "https://dev.matsuostation.com/Freee/Uriage/" + str(yid) + "/"
		html = urlopen(url)
		bsObj = BeautifulSoup(html, "html.parser")

		LastA = bsObj.findAll("div", {"class":"pagination"})[0]("a", {"class":"LastPage"})[0]["href"]

		## (Main)
		# LastPage = int(re.findall('page=([0-9]+)', LastA)[0])
		## (Test)
		LastPage = int(70)

		context['LastPage'] = LastPage


		### *.CSV - File_Check ###
		## SHARP/K/ALL_K_*.CSV : True
		if os.path.exists("SHARP/K/ALL_K_" + str(yid) + ".csv"):
			context['ALL_CSV_Check'] = "True"

			## SHARP/K/ALL_RedCode_*.CSV : True
			if os.path.exists("SHARP/K/ALL_RedCode_" + str(yid) + ".csv"):
				context['ALL_RedCord_Check'] = "True"

				## SHARP/K/ALL_CT_Del_*.CSV : True
				if os.path.exists("SHARP/K/ALL_CT_Del_" + str(yid) + ".csv"):
					context['ALL_Cday_True_Del'] = "True"

					### 掛売上 :
					df_c_9_v = []
					df_c_9, df_c_9_v = CSV_Value_Pull(yid)

					# (OK)
					# (OK) context['df_c_9'] = df_c_9
					# (OK)
					context['df_c_9_list'] = df_c_9.values.tolist()
					context['df_c_9_v'] = df_c_9_v


					## 金額 : 更新
					# df_c_9_vl = []
					df_c_9_vl = df_c_9.reset_index().copy()

					## 金額 & Tax : 更新
					try:
						for i in df_c_9_vl.index:
							if df_c_9_vl.ix[i, "品目"] == "10500":
								df_c_9_vl.loc[i, "税額"] = Decimal(in_tax(float(df_c_9_v[i] * (df_c_9_vl.loc[i, "amount"] / 100)))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
								df_c_9_vl.loc[i, "金額"] = Decimal(float(df_c_9_v[i] * (df_c_9_vl.loc[i, "amount"] / 100))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
							elif df_c_9_vl.ix[i, "品目"] == "10200":
								df_c_9_vl.loc[i, "税額"] = Decimal(in_tax(float((df_c_9_v[i] - 32.1) * (df_c_9_vl.loc[i, "amount"] / 100)))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
								df_c_9_vl.loc[i, "金額"] = Decimal(float(df_c_9_v[i] * (df_c_9_vl.loc[i, "amount"] / 100))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
							else:
								df_c_9_vl.loc[i, "税額"] = Decimal(out_tax(float(df_c_9_v[i] * (df_c_9_vl.loc[i, "amount"] / 100)))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
								df_c_9_vl.loc[i, "金額"] = Decimal(float(df_c_9_v[i] * (df_c_9_vl.loc[i, "amount"] / 100))).quantize(Decimal('0'), rounding=ROUND_HALF_UP) + df_c_9_vl.ix[i, "税額"]

					except Exception as e:
						print(e, 'DF_C.9.Tax.ReMake - Freee/Views.dds : error occured.')


					context['df_c_9_vl'] = df_c_9_vl
					context['df_c_9_tax'] = df_c_9_vl['品目']

					# (OK)
					df_c_9_vl.to_csv("SHARP/K/ALL_C9_OIL_VLTax_" + str(yid) + ".csv", encoding='utf-8', index=0)



				## SHARP/K/ALL_CT_Del_*.CSV : False
				else:
					context['ALL_Cday_True_Del'] = "False"

					## ALL_CT_Del_*.CSV 出力
					# (OK)
					CSV_ALL_CDay_True(yid)
					# (T.OK) df_r_ct_target = CSV_ALL_CDay_True(yid)
					# (T.OK) print(df_r_ct_target.dtypes)
					# (T.OK) context['df_r_ct_target'] = df_r_ct_target


			## SHARP/K/RedCode.CSV : False
			else:
				context['ALL_RedCord_Check'] = "False"

				## ALL_RedCode_*.CSV 出力
				df_rc = CSV_RedCord(yid)


		## SHARP/K/ALL_K_*.CSV : False
		else:
			context['ALL_CSV_Check'] = "False"

			## ALL_K_*.CSV 出力
			with open("SHARP/K/ALL_K_" + str(yid) + ".csv", "w", encoding='utf-8') as file:
				## CSV.出力
				CSV_Write(file, LastPage, url)

		return context


### Uriage_Get ###
def Uriage_Get(request):
	# return HttpResponse("Hello Uriage.Py3 You're at the Uriage.")

	if request.method == 'POST':
		form = YearForm(request.POST)
		yid_post = request.POST['yid']
		if form.is_valid():
			return HttpResponseRedirect('/Freee/Uriage_CSV/%s' % yid_post)

	else:
		form = YearForm()

	return render(request, 'uriage_get.html', {'form': form})


### Uriage_List ###
class Uriage_List(ListView):

	model = Name_Test20
	form_class = YearForm
	template_name = 'uriage_list.html'
	context_object_name = "nametb"
	# paginate_by = 5

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		yid_post = request.POST['yid']

		if form.is_valid():
			return HttpResponseRedirect( '/Freee/Uriage/%s' % yid_post )

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = YearForm()
		yid = self.kwargs.get('yid')
		context['yid'] = yid
		SHARP20_K = 'SHARP20_K_' + str(yid)
		context['SHARP20_K'] = SHARP20_K

		### MySQL:Connection ###
		conn = pymysql.connect(read_default_file='../../ssh/AWS_RDS_Dev.cnf')

		try:
			### MySQL:Session ###
			with conn.cursor() as cursor:
				# sql = "SELECT * FROM SHARP20_K_2019 WHERE m_datetime < %s AND p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"
				# sql = "SELECT * FROM %s " % SHARP20_K + "WHERE m_datetime < %s AND p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"
				# sql = "SELECT * FROM %s " % SHARP20_K + "WHERE p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"
				# sql = "SELECT * FROM %s " % SHARP20_K + "WHERE m_datetime > '2018-08-01' AND p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"
				sql = "SELECT * FROM %s " % SHARP20_K + \
					"WHERE m_datetime > '%s-08-01' " % (yid-1)  + \
					"AND m_datetime < '%s-08-01' " % yid + "AND p_code = %s ORDER BY m_datetime"
					#(OK.現金売上のみ) "AND m_datetime < '%s-08-01' " % yid + "AND p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"

				## 売上高
				cursor.execute(sql,("10"))
				# (OK.現金売上のみ) cursor.execute(sql,("10","0","1",))

				SQL_Data = dictfetchall(cursor)

		finally:
			conn.close()

		### Pager ###
		paginator = Paginator(SQL_Data, 40)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1

		try:
			SQL_Data = paginator.page(page)
		except(EmptyPage, InvalidPage):
			SQL_Data = paginator.page(1)

		context['sqls'] = SQL_Data

		return context


### Uriage ###
def Uriage(request):
	# return HttpResponse("Hello Uriage.Py3 You're at the Uriage.")

	if request.method == 'POST':
		form = YearForm(request.POST)
		yid_post = request.POST['yid']
		if form.is_valid():
			return HttpResponseRedirect('/Freee/Uriage/%s' % yid_post)

	else:
		form = YearForm()

	return render(request, 'uriage.html', {'form': form})


### Index ###
def index(request):
	return HttpResponse("Hello Freee.Py3 You're at the Index.")
