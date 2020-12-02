#//+------------------------------------------------------------------+
#//|                   VerysVeryInc.Python3.Django.nIndex.FreeeAPI.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.nIndex.FreeeApi.py - Ver.3.70.4 Update:2020.12.02" |
#//+------------------------------------------------------------------+
#//|                                                  @datagrid-okada |
#//|               https://github.com/datagrid-okada/python-freee-api |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

### FreeeAPI ###
import requests
import json
import urllib.parse
import time


class Freee():

	def __init__(self, client_id, client_secret, company_id, token_filename):
		self.client_id = client_id
		self.client_secret = client_secret
		self.token_filename = token_filename
		self.company_id = company_id

		self.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
		self.authorize_api_url = 'https://accounts.secure.freee.co.jp/public_api/token'
		self.account_endpoint = "https://api.freee.co.jp/api/1/"
		self.hr_endpoint = "https://api.freee.co.jp/hr/api/v1/"


	# =======================================
	# 	認証系
	# =======================================
	def save_tokens(self, token_dict):
		f = open(self.token_filename, "w")
		json.dump(token_dict, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


	def read_tokens(self):
		with open(self.token_filename) as f:
			return json.load(f)

	def get_access_token(self, authorization_code):

		params = {
			'grant_type': 'authorization_code',
			'client_id': self.client_id,
			'client_secret': self.client_secret,
			'code': authorization_code,
			'redirect_uri': self.redirect_uri
		}

		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		res = requests.post(self.authorize_api_url, params=params, headers=headers)
		
		if res.ok:
			self.save_tokens(res.json())

		else:
			print("client_id, client_secret, authorization_codeのいずれかに不備がある可能性があります。再度認証コードを取得してください")
			raise res.raise_for_status()


	''' ### OK_Test ###
	def __init__(self):
		self.name = ""
		self.age = 0

	def __del__(self):
		print("Thank you")

	def getInfo(self):
		return self.name, self.age

	def setInfo(self, name, age):
		self.name = name
		self.age = age
	''' ### End OK.Test ###

	"""docstring for Freee"""
	# def __init__(self, arg):
	# 	super(Freee, self).__init__()
	# 	self.arg = arg

	''' ### Def.OK ###
	def __init__(self):
		self. name = ""
	''' ### End of Def.OK ###


'''
