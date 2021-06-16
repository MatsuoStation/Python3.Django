#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.cFreee.Views.py - Ver.3.92.3 Update:2021.06.16" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

### Google.API ###
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

def python(request):

	gJsonFile = "../matsuostationapi-d4eecb8e23c3.json"

	spsh_name = "GooglePython"
	ws = connect_gspread(gJsonFile, spsh_name)
	# spsh_key = "186lVOriJXzl_7wIlLxq7jgAxvrGtCq5YtdprnUpdGi4"
	# ws = connect_gspread(gJsonFile, spsh_key)
	# spsh_url = "https://docs.google.com/spreadsheets/d/186lVOriJXzl_7wIlLxq7jgAxvrGtCq5YtdprnUpdGi4/edit#gid=0"
	# ws = connect_gspread(gJsonFile, spsh_url)

	ws.update_cell(1,1,"Test_3.92.2")

	return HttpResponse("Google.Json.File = %s : %s" % (ws.title, ws.id))
	# return HttpResponse("Hello cFreee/Python You're at the Python.")


### Google.API : Connect ###
def connect_gspread(jsonf, spsh):
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
	gc = gspread.authorize(credentials)

	SPREADSHEET_KEY = spsh
	# SPREADSHEET_KEY = key

	worksheet = gc.open(SPREADSHEET_KEY).sheet1
	# worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
	# worksheet = gc.open_by_url(SPREADSHEET_KEY).sheet1

	return worksheet


### Default ###
def index(request):
	return HttpResponse("Hello cFreee/Index.py. You're at the Index.")
