#//+------------------------------------------------------------------+
#//|       VerysVeryInc.Python3.Django.sFreee.Util.Connect_GSpread.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.sFreee.Util.GSp.py - Ver.3.93.3 Update:2021.08.27" |
#//+------------------------------------------------------------------+
### Google.API ###
import gspread
from oauth2client.service_account import ServiceAccountCredentials

### Google.API : Connect ###
def connect_gspread(jsonf, spsh):
	scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
	gc = gspread.authorize(credentials)

	SPREADSHEET_KEY = spsh
	# SPREADSHEET_KEY = key

	worksheet = gc.open(SPREADSHEET_KEY)
	# worksheet = gc.open(SPREADSHEET_KEY).sheet1
	# worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
	# worksheet = gc.open_by_url(SPREADSHEET_KEY).sheet1

	return worksheet

