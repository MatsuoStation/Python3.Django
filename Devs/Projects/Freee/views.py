#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Freee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.24 Update:2019.09.15" |
#//|               https://qiita.com/hujuu/items/b0339404b8b0460087f9 |
#//|                https://qiita.com/mazu/items/77db19ca2caf128cc062 |
#//|                            https://techacademy.jp/magazine/18994 |
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

		### CSV ###
		## SSL
		ssl._create_default_https_context = ssl._create_unverified_context

		## URL
		url = "https://dev.matsuostation.com/Freee/Uriage/" + str(yid) + "/"
		html = urlopen(url)
		# html = urlopen("https://dev.matsuostation.com/Freee/Uriage/" + str(yid) + "/")
		# html = urlopen("https://dev.matsuostation.com/Freee/Uriage/2019/")
		bsObj = BeautifulSoup(html, "html.parser")

		## Table
		# (OK) table = bsObj.findAll("table", {"class":"table"})[0]
		# (OK) rows = table.findAll("tr")

		## LastPage
		# res = requests.get(url)
		# res = requests.get(html, headers=Agent)

		LastA = bsObj.findAll("div", {"class":"pagination"})[0]("a", {"class":"LastPage"})[0]["href"]
		LastPage = int(re.findall('page=([0-9]+)', LastA)[0])

		# (Test) LastPage = int(3)
		# (OK) LastPage = re.findall('[0-9]+', LastA)[0]
		# (OK) LastPage = re.findall('[0-9]+', LastA)
		# LastPage = int(re.findAll(r'page=([0-9]+)[^<]*LastPage',res.text)[0])
		# LastPage = re.search('page=([0-9]+)[^?]*', LastA)
		# LastA = bsObj.findAll("pagination", {"class":"LastPage"})[0]["href"]

		context['LastPage'] = LastPage

		# if LastPage:
			# context['LastPage'] = LastPage
		# context['LastPage'] = print(LastPage)
		# context['LastPage'] = LastA # ?pae=1093&dl=


		## Scraping
		## *.CSV : File_Check
		if os.path.exists("SHARP/K/K_" + str(yid) + ".csv"):
			context['CSV_Check'] = "True"

		else:
			context['CSV_Check'] = "False"

			with open("SHARP/K/K_" + str(yid) + ".csv", "w", encoding='utf-8') as file:
				CSV_Write(file, LastPage, url)

		# with open("SHARP/K/K_" + str(yid) + ".csv", "w", encoding='utf-8') as file:
			# CSV_Write(file, LastPage, url)

			''' (OK) Ver.3.20.23
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
			'''

		''' (OK) Ver.3.20.21
		# with open("SHARP/K/K_2019.csv", "w", encoding='utf-8') as file:
			wr = csv.writer(file)
			for row in rows:
				csvRow = []
				for cell in row.findAll(['td', 'th']):
					csvRow.append(cell.get_text())
				wr.writerow(csvRow)
		'''


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
					"AND m_datetime < '%s-08-01' " % yid + "AND p_code = %s AND r_code IN (%s,%s) ORDER BY m_datetime"

				# cursor.execute(sql,("2018-07-03","10","0","1",))
				# cursor.execute(sql,("2018-07-03","10","0","1",))
				# cursor.execute(sql,("10","0","1",))
				cursor.execute(sql,("10","0","1",))

				SQL_Data = dictfetchall(cursor)
				# context['sqls'] = SQL_Data

				# result = cursor.fetchall()
				# print(result)
				# context['sqls'] = result

		finally:
			conn.close()

		### Pager ###
		paginator = Paginator(SQL_Data, 60)
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
