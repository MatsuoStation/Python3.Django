#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.FreeeAPI.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.FreeeAPI.Views.py - Ver.3.50.3 Update:2020.05.17" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

# Freee_API
from requests_oauthlib import OAuth2Session
import requests
import json




def Test(request):
	# return HttpResponse("Test.Freee.API Page!! Welcome to Devs.MatsuoStation.Com!")

	### Def.API.Authorization.Code
	AUTHORIZATION_CODE = '6604a25e68356c9a4d3987a7a532d573b7e4cb50309db382aa04719f20171c68'

	### (GET) FreeeConfig.Json
	with open("../freeeconfig.json") as fc:
		fc_data = json.load(fc)


	# 事務所一覧.取得用API.URL
	COMPANY_API_URL = fc_data['company_api_url']
	# 取引先一覧.取得用API.URL
	PARTNER_API_URL = fc_data['partner_api_url']


	### (GET) FreeeToken.Json
	with open("../freeetoken.json") as fj:
		fj_data = json.load(fj)

	# (GET) Refresh.Token
	REFRESH_TOKEN = fj_data['refresh_token']
	# (GET) Access.Token
	ACCESS_TOKEN = fj_data['access_token']

	### (GET) Freee.Connect
	# Freee.Session.SetUp
	FreeeOAuth = OAuth2Session()
	FreeeOAuth.headers['Content-Type'] = 'application/json'

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


### Get_A_Token ###
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



def index(request):
	return HttpResponse("Hello FreeeAPI.py. You're at the Index.")
