#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.nIndex.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.nIndex.Views.py - Ver.3.70.4 Update:2020.12.02" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

# Oauth #
import urllib
import json
from oauthlib.oauth2 import WebApplicationClient

# FreeeClient
from .freee_api import Freee 


def FreeeAPI(request):

	### (GET) FreeeConfig.Json
	with open("../freeeconfig.json") as fc:
		fc_data = json.load(fc)

	## Freee.API.Config
	client_id = fc_data['client_id']
	client_secret = fc_data['client_secret']
	company_id = fc_data['company_id']
	authorize_code = fc_data['authorize_code']
	token_filename = "../token.json"

	### OK.Test ###
	# freee = Freee()
	# freee.setInfo("Ayano", 32)
	# print(freee.getInfo())
	# del freee
	### End OK.Test ###

	freee = Freee(client_id, client_secret, company_id, token_filename)
	freee.get_access_token(authorize_code)




	# freee = freee_api.Freee()
	# freee = freee_api.Freee(client_id, client_secret, company_id, token_filename)
	# freee.get_access_token(authorize_code)



	return HttpResponse(token_filename)

def Web_Oauth(request):
	# Freee API #
	FREEE_API_CLIENT_ID = "110f1ecca3b4c84f437df9ea7c8370d3d4d6978195cc9a147803220e6c6f593e"
	FREEE_API_CLIENT_SECRET = "070bc6225a4bf4b68a2256a0b8d056b70d713f8ebab3b99c10d9aecc6b4394cf"
	FREEE_API_REDIRECT_URL = "urn:ietf:wg:oauth:2.0:oob"

	# Web_Oauth - Webアプリ認証用URL
	Web_Oauth = WebApplicationClient(FREEE_API_CLIENT_ID)
	Web_CodeURL, headers, body = Web_Oauth.prepare_authorization_request('https://accounts.secure.freee.co.jp/public_api/authorize', redirect_url = FREEE_API_REDIRECT_URL)

	return HttpResponse(Web_CodeURL)
	# return HttpResponse("Hello Oauth.3.0")


def index(request):
	return HttpResponse("Hello nIndex.py. You're at the nIndex.")
