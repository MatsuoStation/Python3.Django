#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Invoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Dj.Invoice.Views.py - Ver.3.15.3 Update:2019.04.10" |
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
from Finance.models import Invoice_Test20, Name_Test20, Bank_Test20, Value_Test30

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger

from django.utils import dateformat
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Count, Min, Max, Sum, Avg

from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas

jtax = 0.08
ndigits = 0
ktax = 32.1

# Freee_API
from requests_oauthlib import OAuth2Session
import requests
import json


def SS_InTax(value):
	# jtax = 0.08
	# ndigits = 0

	values = value - (value / (1+jtax))
	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		tax_v = int(round(values, 0))
	c = (10 ** d_point) * 2
	tax_v = int(round((values * c + 1) / c, 0))
	sv = value
	notax_v = sv - tax_v

	return sv, tax_v, notax_v


def SS_Values(values):
	# jtax = 0.08
	# ndigits = 0

	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		notax_v = round(values, 0)
	c = (10 ** d_point) * 2
	notax_v = int(round((values * c + 1) / c, 0))

	s_tax = notax_v * jtax
	dd_point = len(str(s_tax).split('.')[1])
	if ndigits >= dd_point:
		tax_v = int(round(s_tax, 0))
	cc = (10 ** dd_point) * 2
	tax_v = int(round((s_tax * cc + 1) / cc, 0))

	sv = notax_v + tax_v

	return sv, tax_v, notax_v


def Keiyu_Values(value, amount):
	# ktax = 32.1
	# jtax = 0.08

	values = (value - ktax) * amount

	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		notax_v = round(values, 0)
	c = (10 ** d_point) * 2
	notax_v = int(round((values * c + 1) / c, 0))

	k_tax = -(-ktax * amount)
	k_tax = int(k_tax)

	ks_tax = notax_v * jtax
	dd_point = len(str(ks_tax).split('.')[1])
	if ndigits >= dd_point:
		tax_v = int(round(ks_tax, 0))
	cc = (10 ** dd_point) * 2
	tax_v = int(round((ks_tax * cc + 1) / cc, 0))

	sv = notax_v + tax_v + k_tax

	return k_tax, sv, tax_v, notax_v


def Toyu_Values(values):

	d_point = len(str(values).split('.')[1])
	if ndigits >= d_point:
		notax_v = round(values, 0)
	c = (10 ** d_point) * 2
	notax_v = int(round((values * c + 1) / c, 0))

	ts_tax = notax_v - (notax_v / (1+jtax))
	dd_point = len(str(ts_tax).split('.')[1])
	if ndigits >= dd_point:
		tax_v = int(round(ts_tax, 0))
	cc = (10 ** dd_point) * 2
	tax_v = int(round((ts_tax * cc + 1) / cc, 0))

	sv = notax_v
	notax_v = notax_v - tax_v

	return sv, tax_v, notax_v


### Freee_API ###
def Get_A_Token(r_code, a_code):

	# new_code = a_code

	### (GET) FreeeConfig.Json
	with open("../freeeconfig.json") as fc:
		fc_data = json.load(fc)
		
	### Freee.API.Config
	CLIENT_ID = fc_data['client_id']
	CLIENT_SECRET = fc_data['client_secret']
	REDIRECT_URI = fc_data['redirect_uri']

	### Freee.API.URL
	# 認証トークン.取得用API.URL
	AUTHORIZE_API_URL = fc_data['authorize_api_url']

	'''
	# 事務所一覧.取得用API.URL
	COMPANY_API_URL = fj_data['company_api_url']
	# 取引先一覧.取得用API.URL
	PARTNER_API_URL = fj_data['partner_api_url']
	'''

	### (GET) Access.Token
	# Freee.OAuth.SetUp
	FreeeOAuth = OAuth2Session()
	FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'

	### REFRESH_TOKEN.True
	if r_code:

		# Refresh.Params
		params = {
			'grant_type' : 'refresh_token',
			'client_id' : CLIENT_ID,
			'client_secret' : CLIENT_SECRET,
			'refresh_token' : r_code
		}

		# FreeeAPI.OAuth2.POST
		r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

		# 正常受信 : 200
		if r.status_code == 200:
			data = json.loads(r.text)

			ACCESS_TOKEN = data['access_token']
			REFRESH_TOKEN = data['refresh_token']

			# (READ) FreeeToken.Json
			R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

			### Refresh.Token.Write ###
			fw = open('../freeetoken.json', 'w')
			fw.write(R_Text)
			fw.close()

			return ACCESS_TOKEN

		# 受信エラー : != 200
		else:
			return a_code

	### REFRESH_TOKEN.False
	else:
		# 1st.Access.Params
		params = {
			'grant_type' : 'authorization_code',
			'client_id' : CLIENT_ID,
			'client_secret' : CLIENT_SECRET,
			'code' : a_code,
			'redirect_uri' : REDIRECT_URI
		}

		# FreeeAPI.OAuth2.POST
		r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

		# 正常受信 : 200
		if r.status_code == 200:
			data = json.loads(r.text)

			ACCESS_TOKEN = data['access_token']
			REFRESH_TOKEN = data['refresh_token']

			# (READ) FreeeToken.Json
			R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

			### Refresh.Token.Write ###
			fw = open('../freeetoken.json', 'w')
			fw.write(R_Text)
			fw.close()

			return ACCESS_TOKEN

		# 受信エラー : != 200
		else:
			return a_code


def Freee_API(request):
	# return HttpResponse("Freee API Page!! Welcome to Devs.MatsuoStation.Com!")

	### Def.API.Authorization.Code
	AUTHORIZATION_CODE = '67acccb6be0b84eb2e054e40fdd1f7e591e970f7972e81192aa51851d9f4f2ef'

	### (GET) FreeeToken.Json
	with open("../freeetoken.json") as fj:
		fj_data = json.load(fj)

	REFRESH_TOKEN = fj_data['refresh_token']
	ACCESS_TOKEN = fj_data['access_token']

	# REFRESH_TOKEN.True
	if REFRESH_TOKEN:
		NEW_A_TOKEN = Get_A_Token(REFRESH_TOKEN, ACCESS_TOKEN)

		return render(request, 'freee_api.html', {
	 				'R_Token'	: REFRESH_TOKEN,
	 				'A_Token'	: NEW_A_TOKEN,
	 				'Data'		: fj_data,
	 			})

	# REFRESH_TOKEN.False
	else:
		NEW_A_TOKEN = Get_A_Token("", AUTHORIZATION_CODE)

		return render(request, 'freee_api.html', {
	 				'A_Token'	: NEW_A_TOKEN,
	 				'Data'		: fj_data,
	 			})


	### (Def) Get_A_Token ###
	# ACCESS_TOKEN = Get_A_Token("a811c5f86d22cee5d4a973a55248ad71d6ec17c3e800cd1b2838161140ebf6e7")
	
	# return render(request, 'freee_api.html', {
	# 			'A_Token'	: ACCESS_TOKEN,
	# 		})

	'''
	### Freee.API.Info
	CLIENT_ID = 'eb49d4914b507bad599241ea5299e2d7d48e2dcb9f6d2260f78f44ec1e6e3cb3'
	CLIENT_SECRET = '5827f959407055068d6704b400966102b01c954ea6236547faf4d5c7745a1d8e'
	REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob' # 開発環境だけ使用する場合はこのURIのままでOK
	AUTHORIZATION_CODE = 'f3a728bc1ec4a78e08a526dcb073f38fc4b18cf3dcc0cfb8e5a2ab89a582da76'

	### API.URL
	# トークン取得用API
	AUTHORIZE_API_URL = 'https://api.freee.co.jp/oauth/token'

	# 事業所一覧の取得用API
	COMPANY_API_URL = 'https://api.freee.co.jp/api/1/companies'
	# 取引先一覧の取得用API
	PARTNER_API_URL = 'https://api.freee.co.jp/api/1/partners'

	

	### (GET) Access.Token
	# params = {}

	## FreeeToken.Json.Check ##
	fj = open("../freeetoken.json", "r")
	fj_data = json.load(fj)
	REFRESH_TOKEN = fj_data['refresh_token']

	# Refresh_Token.True
	if REFRESH_TOKEN:

		FreeeOAuth = OAuth2Session()
		FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'

		params = {
			'grant_type' : 'refresh_token',
			'client_id' : CLIENT_ID,
			'client_secret' : CLIENT_SECRET,
			'refresh_token' : REFRESH_TOKEN
		}

		r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

		# 正常受信 : 200
		if r.status_code == 200:
			data = json.loads(r.text)
			
			ACCESS_TOKEN = data['access_token']
			REFRESH_TOKEN = data['refresh_token']

			
			R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

			### Refresh.Token.OPEN ###
			fw = open('../freeetoken.json', 'w')
			fw.write(R_Text)
			fw.close()

			return render(request, 'freee_api.html', {
				'Data'		: data,
				'A_Token'	: ACCESS_TOKEN,
				'R_Token'	: REFRESH_TOKEN,
		 	})

		 # 受信エラー : != 200 
		else:
			data = json.loads(r.text)
			return render(request, 'freee_api.html', {
				'Data'		: data,
		 	})

		### (Def) REFRESH_TOKEN.True
		# return render(request, 'freee_api.html', {
		#	'Data'	: fj_data,
		#	'R_Token'	: REFRESH_TOKEN,
		# })

	# Refresh_Token.False
	else:
		FreeeOAuth = OAuth2Session()
		FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'

		params = {
			'grant_type' : 'authorization_code',
			'client_id' : CLIENT_ID,
			'client_secret' : CLIENT_SECRET,
			'code' : AUTHORIZATION_CODE,
			'redirect_uri' : REDIRECT_URI
		}

		r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

		# 正常受信 : 200
		if r.status_code == 200:
			data = json.loads(r.text)
			
			ACCESS_TOKEN = data['access_token']
			REFRESH_TOKEN = data['refresh_token']

			
			R_Text = '{\n' + '"refresh_token" : "' + REFRESH_TOKEN + '",\n' + '"access_token" : "' + ACCESS_TOKEN + '"\n}'

			### Refresh.Token.OPEN ###
			fw = open('../freeetoken.json', 'w')
			fw.write(R_Text)
			fw.close()

			return render(request, 'freee_api.html', {
				'Data'		: data,
				'A_Token'	: ACCESS_TOKEN,
				'R_Token'	: REFRESH_TOKEN,
		 	})

		# 受信エラー : != 200 
		else:
			data = json.loads(r.text)
			return render(request, 'freee_api.html', {
				'Data'		: data,
		 	})

		# return render(request, 'freee_api.html', {
		#	'Data'	: fj_data,
		# })
	

	### (Def) REFRESH_TOKEN.False
	# return render(request, 'freee_api.html', {
	#		'Data'	: f_data,
	#		'R_Token'	: REFRESH_TOKEN,
	# })

	
	FreeeOAuth = OAuth2Session()
	FreeeOAuth.headers['Content-Type'] = 'application/x-www-form-urlencoded'	

	params = {
			'grant_type' : 'authorization_code',
			'client_id' : CLIENT_ID,
			'client_secret' : CLIENT_SECRET,
			'code' : AUTHORIZATION_CODE,
			'redirect_uri' : REDIRECT_URI
	}

	r = FreeeOAuth.post(AUTHORIZE_API_URL, params=params)

	# return render(request, 'freee_api.html',{ 'Data': r })

	if r.status_code == 200:
		data = json.loads(r.text)

		ACCESS_TOKEN = data['access_token']
		REFRESH_TOKEN = data['refresh_token']
		R_Text = "{\n" + "refresh_token:" + REFRESH_TOKEN + ",\n" + "access_token:" + ACCESS_TOKEN + ",\n" "}"

		### Refresh.Token.OPEN ###
		f = open('../freeetoken.json', 'w')
		f.write(R_Text)
		f.close()

		return render(request, 'freee_api.html',
			{
				'Data'		: data,
				# 'Data'		: R_Text,
				'A_Token'	: ACCESS_TOKEN,
				'R_Token'	: REFRESH_TOKEN,
			})
	else:
		data = json.loads(r.text)
		return render(request, 'freee_api.html',
			{
				'Data'		: data,
			})

	
	# (Def) #
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}

	r = requests.post(AUTHORIZE_API_URL, params=params, headers=headers)
	data = r.json()
	'''


### SxS_List ###
class SxS_List(ListView):

	model = Name_Test20
	form_class = NameForm
	template_name = 'sxs_list.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']

		if form.is_valid():
			return HttpResponseRedirect( '/Invoice/%s' % nid_post )

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		### Guest Search Form ###
		context['form'] = NameForm()
		gid = self.kwargs.get('nid')
		context['gid'] = gid

		### Total Value Cash ###
		dd_list = list()		# 期日リスト
		before_list = list()	# 先月リスト


		### DL : True ###
		try:
			### 初期設定
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')

			### URL.期日
			dd = dlt.day

			## dd : 20日締日 or 25日締日
			if dd == 20 or dd == 25:
				dld = dlt + timedelta(days=1) - relativedelta(months=1)
				dlm = dlt + timedelta(days=1) - timedelta(microseconds=1)

				bld = dld - relativedelta(months=1)
				blm = dlm - relativedelta(months=1)

			## dd : 末日締日
			else:
				dt = dlt - relativedelta(months=1)
				dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
				dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)

				bld = dt - timedelta(days=dt.day) + timedelta(days=1)
				blm = bld  + relativedelta(months=1) - timedelta(microseconds=1)


			### MySQL : データ取得
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')


			### 請求書.日付順
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			### 締日.Check
			try:
				# MySQL.Bankデータ.有無
				if BFs:
					d_values = BFs

				# Invoice.データ
				for dlm in dlms:
					# POS.取引日
					dd = dlm.day

					# MySQL.Bankデータ
					for d in d_values:
						# 顧客別.締切日
						dv = d.check_day

						# 取引日別.月期間
						# 25日以降.取引日
						if dv == 25:
							if dd >=25:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以降.取引日
						elif dv == 20:
							if dd >= 20:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以前.取引日
						else:
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

						# 月期間.リスト
						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds

			### Error表示 : 締日.Check
			except Exception as e:
				print(e, 'DL.True - Invoice/views.dds : error occured.')


			### 期間表示
			dlb = dlt + timedelta(days=1) - relativedelta(months=1)
			context['dlb'] = dlb
			dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
			context['dla'] = dla

			### 顧客氏名
			for na in NAs:
				names = na.name

			### Bank.請求書フォーマット
			for bf in BFs:
				fSS = bf.s_format
				context['fSS'] = fSS

				# 請求書フォーマット:BackImage.Setup
				if fSS == 0:
					# fURL = "background-image: url('https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_30_02.png');"
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
				if fSS == 10:
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
				context['fURL'] = fURL

			### PDF.リンク
			PDF_Link = "../PDF/%s/" % gid
			context['pLink'] = PDF_Link


		### DL : False ###
		except Exception as e:

			### MySQL : データ取得
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')

			### 請求書.日付順
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			### 締日.Check
			try:
				# MySQL.Bankデータ.有無
				if BFs:
					d_values = BFs

				# Invoice.データ
				for dlm in dlms:
					# POS.取引日
					dd = dlm.day

					# MySQL.Bankデータ
					for d in d_values:
						# 顧客別.締切日
						dv = d.check_day

						# 取引日別.月期間
						# 25日以降.取引日
						if dv == 25:
							if dd >=25:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以降.取引日
						elif dv == 20:
							if dd >= 20:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以前.取引日
						else:
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

						# 月期間.リスト
						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds

			### Error表示 : 締日.Check
			except Exception as e:
				print(e, 'DL.False - Invoice/views.dds : error occured.')

			### 顧客氏名
			for na in NAs:
				names = na.name

			### Error表示 : DL.False ###
			print(e, 'Invoice/Views - DL.False : error occured.')

		### ALL.Context ###
		context['names'] = names

		return context


### SS_List ###
class SS_List(ListView):

	model = Name_Test20
	form_class = NameForm
	template_name = 'ss_list.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']

		if form.is_valid():
			return HttpResponseRedirect( '/Invoice/%s' % nid_post )

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = NameForm()
		gid = self.kwargs.get('nid')
		context['gid'] = gid

		### Total Value Cash ###
		dd_list = list()

		incash_list = list()

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

		before_list = list()

		### DL : True ###
		try:
			dl = self.request.GET.get('dl', '')
			dlt = datetime.strptime(dl, '%Y-%m-%d')

			# URL.期日
			dd = dlt.day

			# dd : 20日締日 or 25日締日
			if dd == 20 or dd == 25:
				dld = dlt + timedelta(days=1) - relativedelta(months=1)
				dlm = dlt + timedelta(days=1) - timedelta(microseconds=1)

				bld = dld - relativedelta(months=1)
				blm = dlm - relativedelta(months=1)

			# dd : 末日締日
			else:
				dt = dlt - relativedelta(months=1)
				dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
				dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)

				bld = dt - timedelta(days=dt.day) + timedelta(days=1)
				blm = bld  + relativedelta(months=1) - timedelta(microseconds=1)

			### MySQL : データ取得
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=bld, m_datetime__lte=blm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			# 請求書.日付順
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			### LastDay : Check ###
			try:
				# MySQL.Bankデータ.有無
				if BFs:
					d_values = BFs

				# Invoice.データ
				for dlm in dlms:
					# POS.取引日
					dd = dlm.day

					# MySQL.Bankデータ
					for d in d_values:
						# 顧客別.締切日
						dv = d.check_day

						# 取引日別.月期間
						# 25日以降.取引日
						if dv == 25:
							if dd >=25:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以降.取引日
						elif dv == 20:
							if dd >= 20:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以前.取引日
						else:
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

						# 月期間.リスト
						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds


			### LastDay : Check.Error ###
			except Exception as e:
				print(e, 'Invoice/views.dds : error occured')


			### Bank.請求書フォーマット ###
			for bf in BFs:
				fSS = bf.s_format
				context['fSS'] = fSS

				# 請求書フォーマット:BackImage.Setup
				if fSS == 0:
					# fURL = "background-image: url('https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_30_02.png');"
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
				if fSS == 10:
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
				context['fURL'] = fURL

			### PDF.リンク ###
			PDF_Link = "../PDF/%s/" % gid
			context['pLink'] = PDF_Link

			### 氏名 ###
			for na in NAs:
				names = na.name

			### 期間表示 ###
			dlb = dlt + timedelta(days=1) - relativedelta(months=1)
			context['dlb'] = dlb
			dla = dlt + timedelta(days=1) - timedelta(microseconds=1)
			context['dla'] = dla

			### 現金入金.Incash Total Cash ###
			for iv in IVs:
				if iv.s_code.uid == "00000":
					incash_list.append(iv.value)
					incash_values = sum(incash_list)
					context['incash_values'] = incash_values

			### Caluculate ###
			try:
				### Select Month ###
				for iv in IVs:
					# 現金関係 & 振込関係
					if iv.s_code.uid == "00000":
						sv = 0
						total_list.append(sv)
					elif iv.s_code.uid == "00002":
						sv = 0
						total_list.append(sv)

					# 金額(税別金額) : True
					elif iv.value:
						# 単価 : True
						if iv.unit != 0:
							# (SHARP.POS : 基本設定<税別>)
							notax_v = iv.value
							tax_v = iv.tax_v
							sv = notax_v + tax_v

							if iv.red_code:
								notax_v = -(notax_v)
								tax_v = -(tax_v)
								sv = -(sv)

					# 金額(税別金額) : False
					else:
						# 税金 : True
						if iv.tax != 0:
							tax_v = iv.tax
							notax_v = iv.value
							sv = notax_v + tax_v

				### 総額 ###


				### End of Select Month ###



			### Caluculate.Error ###
			except Exception as e:
				print(e, 'Invoice/views.Caluculate : error occured')


		### DL : False ###
		except Exception as e:

			### MySQL : データ取得
			IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			NAs = Name_Test20.objects.all().filter(uid=self.kwargs.get('nid'))
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			# 請求書.日付順
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			### LastDay : Check ###
			try:
				# MySQL.Bankデータ.有無
				if BFs:
					d_values = BFs

				# Invoice.データ
				for dlm in dlms:
					# POS.取引日
					dd = dlm.day

					# MySQL.Bankデータ
					for d in d_values:
						# 顧客別.締切日
						dv = d.check_day

						# 取引日別.月期間
						# 25日以降.取引日
						if dv == 25:
							if dd >=25:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以降.取引日
						elif dv == 20:
							if dd >= 20:
								dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) + timedelta(days=dv-1)
							else:
								dls = (dlm - timedelta(days=dd-1)) + timedelta(days=dv-1)
						# 20日以前.取引日
						else:
							dls = (dlm - timedelta(days=dd-1)) + relativedelta(months=1) - timedelta(days=1)

						# 月期間.リスト
						dd_list.append(dls)
						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
						context['dds'] = dds



			### LastDay : Check.Error ###
			except Exception as e:
				print(e, 'Invoice/views.dds : error occured')

			### 氏名 ###
			for na in NAs:
				names = na.name

			print(e, 'Invoice/Views - DL.False : error occured')

		### ALL.Context ###
		context['names'] = names
		context['ivs'] = IVs

		return context


### Invoice_List ###
class Invoice_List(ListView):

	model = Name_Test20
	# model = SHARP_Test
	form_class = NameForm
	template_name = 'list.html'
	# template_name = 'index.html'
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

				bld = dld - relativedelta(months=1)
				blm = dlm - relativedelta(months=1)

			else:
				dt = dlt - relativedelta(months=1)
				dld = dt + relativedelta(months=1) - timedelta(days=dt.day) + timedelta(days=1)
				dlm = dld + relativedelta(months=1) - timedelta(microseconds=1)

				bld = dt - timedelta(days=dt.day) + timedelta(days=1)
				blm = bld  + relativedelta(months=1) - timedelta(microseconds=1)


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
			bIVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=bld, m_datetime__lte=blm).select_related('g_code').select_related('s_code').order_by('car_code', 'm_datetime')
			# (Def.Order.Date) IVs = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid'), m_datetime__gte=dld, m_datetime__lte=dlm).select_related('g_code').select_related('s_code').order_by('m_datetime', 'car_code',)
			names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')
			# months = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct()
			# months = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct()
			lastmonths = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code').select_related('s_code').values_list('m_datetime', flat=True).order_by('-m_datetime').distinct('m_datetime')
			VLs = Value_Test30.objects.filter(uid=self.kwargs.get('nid')).order_by('s_code')
			BFs = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			# check_days = Bank_Test20.objects.all().filter(uid=self.kwargs.get('nid'))

			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')

			context['dlms'] = dlms

			# (Check) context['bld'] = bld
			# (Check) context['blm'] = blm

			### Bank.請求書フォーマット ###
			for bf in BFs:
				fLPG = bf.s_format
				context['fLPG'] = fLPG

				# 請求書フォーマット:BackImage.Setup
				if fLPG == 0:
					# fURL = "background-image: url('https://dev.matsuostation.com/static/images/LPG/New_Seikyu_LPG_30_02.png');"
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_0_02.png"
				if fLPG == 10:
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_10_02.png"
				if fLPG == 20:
					fURL = "https://dev.matsuostation.com/static/images/Invoice/New_Seikyu_SS_20_02.png"
				context['fURL'] = fURL


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

			before_list = list()

			# ndigits = 0
			# jtax = 0.08

			### Caluculate ###
			try:
				### Select Month ###
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

								# total_list.append(sv)
								# notax_list.append(notax_v)
								# tax_list.append(tax_v)

								### Unit Int Check
								if iv.s_code.uid == "10500":
									# t_amount = iv.amount/100

									ta = iv.amount/100
									uc = sv / ta

									if uc.is_integer():
										t_amount = iv.amount/100
										if iv.red_code:
											t_amount = -(t_amount)
										#	notax_v = -(notax_v)
										#	sv = -(sv)
										#	tax_v = -(tax_v)

									else:
										# t_amount = 1
										t_amount = iv.amount/100
										sv, tax_v, notax_v = SS_InTax(notax_v)

										'''
										values = notax_v - (notax_v / (1+jtax))
										d_point = len(str(values).split('.')[1])
										if ndigits >= d_point:
											tax_v = int(round(values, 0))
										c = (10 ** d_point) * 2
										tax_v = int(round((values * c + 1) / c, 0))
										sv = notax_v
										notax_v = notax_v - tax_v
										'''

										if iv.red_code:
											t_amount = -(t_amount)
										#	tax_v = -(tax_v)
										#	sv = -(sv)
										#	notax_v = -(notax_v)

									toyu_a_list.append(t_amount)
									toyu_list.append(notax_v)

								total_list.append(sv)
								notax_list.append(notax_v)
								tax_list.append(tax_v)

							### 税金 : False
							else:
								# 灯油 = "10500"
								if iv.s_code.uid == "10500":
									sv, tax_v, notax_v = SS_InTax(iv.value)

									'''
									values = iv.value - (iv.value / (1+jtax))
									d_point = len(str(values).split('.')[1])
									if ndigits >= d_point:
										tax_v = int(round(values, 0))
									c = (10 ** d_point) * 2
									tax_v = int(round((values * c + 1) / c, 0))
									sv = iv.value
									notax_v = sv - tax_v
									'''

									ta = iv.amount/100
									uc = sv / ta

									if uc.is_integer():
										t_amount = ta

										if iv.red_code:
											t_amount = -(t_amount)
											notax_v = -(notax_v)
											sv = -(sv)
											tax_v = -(tax_v)
									else:
										t_amount = ta
										sv, tax_v, notax_v = SS_InTax(notax_v)

										'''
										values = notax_v - (notax_v / (1+jtax))
										d_point = len(str(values).split('.')[1])
										if ndigits >= d_point:
											tax_v = int(round(values, 0))
										tax_v = int(round((values * c + 1) / c, 0))
										sv = notax_v
										notax_v = notax_v - tax_v
										'''

										if iv.red_code:
											t_amount = -(t_amount)
											tax_v = -(tax_v)
											sv = -(sv)
											notax_v = -(notax_v)

									toyu_a_list.append(t_amount)
									toyu_list.append(notax_v)

								# 灯油 : False
								else:
									sv, tax_v, notax_v = SS_InTax(iv.value)

									'''
									values = iv.value - (iv.value / (1+jtax))
									d_point = len(str(values).split('.')[1])
									if ndigits >= d_point:
										tax_v = int(round(values, 0))
									c = (10 ** d_point) * 2
									tax_v = int(round((values * c + 1) / c, 0))
									sv = iv.value
									notax_v = sv - tax_v
									'''

									if iv.red_code:
										tax_v = -(tax_v)
										sv = -(sv)
										notax_v = -(notax_v)

								tax_list.append(tax_v)
								notax_list.append(notax_v)
								total_list.append(sv)



					### 金額 : False
					### Now ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, m_datetime__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, m_datetime__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								# ks_values = (v.value - 32.1) * k_amount
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value, k_amount)

								'''
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
								'''

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
								sv, tax_v, notax_v = SS_Values(hs_values)

								'''
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
								'''

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
								sv, tax_v, notax_v = SS_Values(rs_values)

								'''
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
								'''

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


						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								'''
								d_point = len(str(ts_values).split('.')[1])
								if ndigits >= d_point:
									ts_value = round(ts_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ts_values * c + 1) / c, 0))

								ts_tax = notax_v - (notax_v / (1+jtax))
								dd_point = len(str(ts_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ts_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ts_tax * cc + 1) / cc, 0))

								sv = notax_v
								notax_v = notax_v - tax_v
								'''

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)


					### Date01 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date01__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date01__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								# ks_values = (v.value01 - 32.1) * k_amount
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value01, k_amount)

								'''
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
								'''

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
								sv, tax_v, notax_v = SS_Values(hs_values)

								'''
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
								'''

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
								sv, tax_v, notax_v = SS_Values(rs_values)

								'''
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
								'''

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value01 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								'''
								d_point = len(str(ts_values).split('.')[1])
								if ndigits >= d_point:
									ts_value = round(ts_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ts_values * c + 1) / c, 0))

								ts_tax = notax_v - (notax_v / (1+jtax))
								dd_point = len(str(ts_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ts_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ts_tax * cc + 1) / cc, 0))

								sv = notax_v
								notax_v = notax_v - tax_v
								'''

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date02 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date02__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date02__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								# ks_values = (v.value02 - 32.1) * k_amount
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value02, k_amount)

								'''
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
								'''

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
								hs_values = v.value02 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								'''
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
								'''

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
								rs_values = v.value02 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								'''
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
								'''

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value02 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								'''
								d_point = len(str(ts_values).split('.')[1])
								if ndigits >= d_point:
									ts_value = round(ts_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ts_values * c + 1) / c, 0))

								ts_tax = notax_v - (notax_v / (1+jtax))
								dd_point = len(str(ts_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ts_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ts_tax * cc + 1) / cc, 0))

								sv = notax_v
								notax_v = notax_v - tax_v
								'''

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date03 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date03__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date03__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":
							# k_tax = 1
							# ktax_list.append(k_tax)

							for v in v_values:
								k_amount = iv.amount / 100
								# ks_values = (t.value01 - 32.1) * (iv.amount / 100)
								# ks_values = (v.value03 - 32.1) * k_amount
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value03, k_amount)

								'''
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
								'''

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
								hs_values = v.value03 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								'''
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
								'''

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
								rs_values = v.value03 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								'''
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
								'''

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value03 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								'''
								d_point = len(str(ts_values).split('.')[1])
								if ndigits >= d_point:
									ts_value = round(ts_values, 0)
								c = (10 ** d_point) * 2
								notax_v = int(round((ts_values * c + 1) / c, 0))

								ts_tax = notax_v - (notax_v / (1+jtax))
								dd_point = len(str(ts_tax).split('.')[1])
								if ndigits >= dd_point:
									tax_v = int(round(ts_tax, 0))
								cc = (10 ** dd_point) * 2
								tax_v = int(round((ts_tax * cc + 1) / cc, 0))

								sv = notax_v
								notax_v = notax_v - tax_v
								'''

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date04 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date04__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date04__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value04, k_amount)

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
								hs_values = v.value04 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value04 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value04 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date05 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date05__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date05__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value05, k_amount)

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
								hs_values = v.value05 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value05 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value05 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date06 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date06__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date06__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value06, k_amount)

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
								hs_values = v.value06 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value06 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value06 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date07 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date07__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date07__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value07, k_amount)

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
								hs_values = v.value07 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value07 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value07 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date08 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date08__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date08__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value08, k_amount)

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
								hs_values = v.value08 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value08 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value08 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date09 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date09__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date09__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value09, k_amount)

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
								hs_values = v.value09 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value09 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value09 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date10 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date10__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date10__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value10, k_amount)

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
								hs_values = v.value10 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value10 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value10 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date11 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date11__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date11__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value11, k_amount)

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
								hs_values = v.value11 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value11 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value11 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date12 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date12__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date12__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value12, k_amount)

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
								hs_values = v.value12 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value12 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value12 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date13 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date13__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date13__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value13, k_amount)

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
								hs_values = v.value13 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value13 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value13 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date14 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date14__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date14__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value14, k_amount)

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
								hs_values = v.value14 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value14 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value14 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date15 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date15__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date15__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value15, k_amount)

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
								hs_values = v.value15 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value15 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value15 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date16 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date16__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date16__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value16, k_amount)

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
								hs_values = v.value16 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value16 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value16 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date17 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date17__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date17__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value17, k_amount)

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
								hs_values = v.value17 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value17 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value17 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date18 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date18__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date18__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value18, k_amount)

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
								hs_values = v.value18 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value18 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value18 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)
					### Date19 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date19__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date19__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value19, k_amount)

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
								hs_values = v.value19 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value19 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value19 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date20 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date20__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date20__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value20, k_amount)

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
								hs_values = v.value20 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value20 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value20 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date21 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date21__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date21__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value21, k_amount)

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
								hs_values = v.value21 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value21 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value21 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date22 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date22__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date22__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value22, k_amount)

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
								hs_values = v.value22 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value22 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value22 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date23 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date23__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date23__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value23, k_amount)

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
								hs_values = v.value23 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value23 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value23 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date24 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date24__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date24__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value24, k_amount)

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
								hs_values = v.value24 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value24 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value24 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Date25 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date25__lte=iv.m_datetime):
						v_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=iv.s_code.uid, date25__lte=iv.m_datetime)

						# 軽油 = "10200"
						if iv.s_code.uid == "10200":

							for v in v_values:
								k_amount = iv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(v.value25, k_amount)

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
								hs_values = v.value25 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

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
								rs_values = v.value25 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

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

						# 灯油 = "10500"
						elif iv.s_code.uid == "10500":
							for v in v_values:
								t_amount = iv.amount/100
								ts_values = v.value25 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if iv.red_code:
									t_amount = -(t_amount)
									notax_v = -(notax_v)
									tax_v = -(tax_v)
									sv = -(sv)

								notax_list.append(notax_v)
								tax_list.append(tax_v)
								total_list.append(sv)

								toyu_a_list.append(t_amount)
								toyu_list.append(notax_v)

					### Another.Date ###
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

				### End of Select Month ###

				### Next Month ###
				for biv in bIVs:
					### 現金関係 & 振込関係
					if biv.s_code.uid == "00000":
						sv = 0
						before_list.append(sv)
					elif biv.s_code.uid == "00002":
						sv = 0
						before_list.append(sv)

					### 金額 : True
					elif biv.value:
						### 単価 : True
						if biv.unit != 0:
							notax_v = biv.value
							tax_v = biv.tax
							sv = notax_v + tax_v

							if biv.red_code:
								notax_v = -(notax_v)
								tax_v = -(tax_v)
								sv = -(sv)

							before_list.append(sv)

						### 単価 : False
						else:
							### 税金 : True
							if biv.tax != 0:
								tax_v = biv.tax
								notax_v = biv.value
								sv = notax_v + tax_v

								if biv.red_code:
									tax_v = -(tax_v)
									notax_v = -(notax_v)
									sv = -(sv)

								# before_list.append(sv)

								### Unit Int Check
								if biv.s_code.uid == "10500":

									ta = biv.amount/100
									uc = sv / ta

									if uc.is_integer():
										t_amount = biv.amount/100
										if biv.red_code:
											t_amount = -(t_amount)

									else:
										t_amount = biv.amount/100
										sv, tax_v, notax_v = SS_InTax(notax_v)

								before_list.append(sv)


							### 税金 : False
							else:
								# 灯油 = "10500"
								if biv.s_code.uid == "10500":
									sv, tax_v, notax_v = SS_InTax(biv.value)

									ta = biv.amount/100
									uc = sv / ta

									if uc.is_integer():
										t_amount = ta

										if biv.red_code:
											# t_amount = -(t_amount)
											# notax_v = -(notax_v)
											sv = -(sv)
											# tax_v = -(tax_v)

									else:
										t_amount = ta
										sv, tax_v, notax_v = SS_InTax(notax_v)

										if biv.red_code:
											# t_amount = -(t_amount)
											# tax_v = -(tax_v)
											sv = -(sv)
											# notax_v = -(notax_v)

								# 灯油 : False
								else:
									sv, tax_v, notax_v = SS_InTax(biv.value)

									if biv.red_code:
										# tax_v = -(tax_v)
										sv = -(sv)
										# notax_v = -(notax_v)

								before_list.append(sv)

								'''
								sv, tax_v, notax_v = SS_InTax(biv.value)

								if biv.red_code:
									tax_v = -(tax_v)
									sv = -(sv)
									notax_v = -(notax_v)

								before_list.append(sv)
								'''

					### 金額 : False
					### Now ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, m_datetime__lte=biv.m_datetime):
						bv_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, m_datetime__lte=biv.m_datetime)

						# 軽油 = "10200"
						if biv.s_code.uid == "10200":
							for bv in bv_values:
								k_amount = biv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(bv.value, k_amount)

								if biv.red_code:
									# notax_v = -(notax_v)
									# k_amount = -(k_amount)
									# k_tax = -(k_tax)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# ハイオク = "10000"
						elif biv.s_code.uid == "10000":
							for bv in bv_values:
								h_amount = biv.amount / 100
								hs_values = bv.value * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								if biv.red_code:
									# h_amount = -(h_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# レギュラー = "10100"
						elif biv.s_code.uid == "10100":
							for bv in bv_values:
								r_amount = biv.amount / 100
								rs_values = bv.value * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								if biv.red_code:
									# r_amount = -(r_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# 灯油 = "10500"
						elif biv.s_code.uid == "10500":
							for bv in bv_values:
								t_amount = biv.amount/100
								ts_values = bv.value * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if biv.red_code:
									# t_amount = -(t_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

					### Date01 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date01__lte=biv.m_datetime):
						bv_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date01__lte=biv.m_datetime)

						# 軽油 = "10200"
						if biv.s_code.uid == "10200":
							for bv in bv_values:
								k_amount = biv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(bv.value01, k_amount)

								if biv.red_code:
									# notax_v = -(notax_v)
									# k_amount = -(k_amount)
									# k_tax = -(k_tax)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# ハイオク = "10000"
						elif biv.s_code.uid == "10000":
							for bv in bv_values:
								h_amount = biv.amount / 100
								hs_values = bv.value01 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								if biv.red_code:
									# h_amount = -(h_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# レギュラー = "10100"
						elif biv.s_code.uid == "10100":
							for bv in bv_values:
								r_amount = biv.amount / 100
								rs_values = bv.value01 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								if biv.red_code:
									# r_amount = -(r_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# 灯油 = "10500"
						elif biv.s_code.uid == "10500":
							for bv in bv_values:
								t_amount = biv.amount/100
								ts_values = bv.value01 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if biv.red_code:
									# t_amount = -(t_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

					### Date02 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date02__lte=biv.m_datetime):
						bv_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date02__lte=biv.m_datetime)

						# 軽油 = "10200"
						if biv.s_code.uid == "10200":
							for bv in bv_values:
								k_amount = biv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(bv.value02, k_amount)

								if biv.red_code:
									# notax_v = -(notax_v)
									# k_amount = -(k_amount)
									# k_tax = -(k_tax)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# ハイオク = "10000"
						elif biv.s_code.uid == "10000":
							for bv in bv_values:
								h_amount = biv.amount / 100
								hs_values = bv.value02 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								if biv.red_code:
									# h_amount = -(h_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# レギュラー = "10100"
						elif biv.s_code.uid == "10100":
							for bv in bv_values:
								r_amount = biv.amount / 100
								rs_values = bv.value02 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								if biv.red_code:
									# r_amount = -(r_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# 灯油 = "10500"
						elif biv.s_code.uid == "10500":
							for bv in bv_values:
								t_amount = biv.amount/100
								ts_values = bv.value02 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if biv.red_code:
									# t_amount = -(t_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

					### Date03 ###
					elif Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date03__lte=biv.m_datetime):
						bv_values = Value_Test30.objects.all().filter(uid=self.kwargs.get('nid'), s_code=biv.s_code.uid, date03__lte=biv.m_datetime)

						# 軽油 = "10200"
						if biv.s_code.uid == "10200":
							for bv in bv_values:
								k_amount = biv.amount / 100
								k_tax, sv, tax_v, notax_v = Keiyu_Values(bv.value03, k_amount)

								if biv.red_code:
									# notax_v = -(notax_v)
									# k_amount = -(k_amount)
									# k_tax = -(k_tax)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# ハイオク = "10000"
						elif biv.s_code.uid == "10000":
							for bv in bv_values:
								h_amount = biv.amount / 100
								hs_values = bv.value03 * h_amount
								sv, tax_v, notax_v = SS_Values(hs_values)

								if biv.red_code:
									# h_amount = -(h_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# レギュラー = "10100"
						elif biv.s_code.uid == "10100":
							for bv in bv_values:
								r_amount = biv.amount / 100
								rs_values = bv.value033 * r_amount
								sv, tax_v, notax_v = SS_Values(rs_values)

								if biv.red_code:
									# r_amount = -(r_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

						# 灯油 = "10500"
						elif biv.s_code.uid == "10500":
							for bv in bv_values:
								t_amount = biv.amount/100
								ts_values = bv.value03 * t_amount
								sv, tax_v, notax_v = Toyu_Values(ts_values)

								if biv.red_code:
									# t_amount = -(t_amount)
									# notax_v = -(notax_v)
									# tax_v = -(tax_v)
									sv = -(sv)

								before_list.append(sv)

					else:
						sv = 0
						before_list.append(sv)

				before_values = sum(before_list)
				context['before_values'] = before_values
				### End of Next Month ###

			except Exception as e:
				print(e, 'Invoice/views.total_values - in_dl : error occured')

			### End of Caluculate ###


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

						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)

						# context['dd'] = dd_list
						context['dds'] = dds

			except Exception as e:
				print(e, 'Invoice/views.py_dds : error occured')

			### End of LastDay : Check ###


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

						dds = sorted(set(dd_list), key=dd_list.index, reverse=True)

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
		# values = Value_Test30.objects.all().filter(uid__endswith=self.kwargs.get('nid'), s_code="10100")

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