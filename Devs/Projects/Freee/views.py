#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Freee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.60 Update:2019.09.29" |
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
	df_rc = df[df['red_code'] == 8]

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
	df_r = pd.read_csv("SHARP/K/ALL_RedCode_" + str(yid) + ".csv", sep=',', usecols=['CDay','CNo','品目'], dtype={'管理番号':'object','取引先':'object','CNo':'object','決済金額':'object'}, encoding='utf-8')

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
		df_r_ct_target_i.append(df_k.reset_index().query('発生日==@x[1] & 管理番号==@x[2] & 品目==@x[0]').index[0])
	# (OK) context['df_r_ct_target_i'] = df_r_ct_target_i


	## Mine :
	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List)) - 抽出
	df_r_ct_mine = df_k[df_k['CDay'].astype('str').str.contains("201")]

	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List) - 行数
	df_r_ct_mine_l = len(df_r_ct_mine)
	# (OK) context['df_r_ct_mine_len'] = df_r_ct_mine_l

	# Mine : ALL_RedCode_*.CSV : 自リスト(Mine_List) - 削除Index
	df_r_ct_mine_i = df_k[df_k['CDay'].astype('str').str.contains("201")].index
	# (OK) context['df_r_ct_mine_i'] = df_r_ct_mine_i

	## Target & Mine : Delete後 - CSV.出力
	df_r_ct_t = df_k.drop(df_r_ct_target_i)
	df_r_ct_m = df_r_ct_t.drop(df_r_ct_mine_i)
	df_r_ct_m.to_csv("SHARP/K/ALL_CT_Del_" + str(yid) + ".csv", encoding='utf-8', index=0)


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
		LastPage = int(30)

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

				else:
					context['ALL_Cday_True_Del'] = "False"

					## ALL_CT_Del_*.CSV 出力
					CSV_ALL_CDay_True(yid)


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
