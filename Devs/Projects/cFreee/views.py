#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|     "VsV.Py3.Dj.cFreee.Views.py - Ver.3.92.22 Update:2021.08.26" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

### Google.API ###
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from .forms import NameForm, BankForm
from Finance.models import Name_Test20, Bank_Test20, SHARPnPOS
from .Util.db_cinvoice import DB_cInvoice, DB_Address, GAS_SpSh_Name
from .Util.deadline import DeadLine, DeadLine_List


### cInvoice_List ###
class cInvoice_List(ListView):
	model = SHARPnPOS
	form_class = NameForm
	template_name = 'clist.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/cFreee/cInvoice/%s' % nid_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## Search : g_code ##
		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		## DeadLine : Setup ##
		dd_list = list()

		## * try: * dl = Ture ##
		try:
			dl = self.request.GET.get('dl', '')
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			dd = dlstr.day  # DeadLine : Day
			dld, dlm, dlb, dla, bld, blm = DeadLine(dd, dlstr)

			## DB : Setup ##
			names, IVs, bIVs, lastmonths, BFs = DB_cInvoice(self, dld, dlm, bld, blm)

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			try:
				if BFs:
					d_values = BFs
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=True / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			context['dlb'] = dlb
			context['dla'] = dla
			## End of LastDay : Check (dl = True) ##

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

			## DB : Setup ##
			names, IVs, bIVs, lastmonths, BFs = DB_cInvoice(self, "", "", "", "")

			## DeadLine : Month & Secconde
			dlms = lastmonths.dates('m_datetime', 'day', order='ASC')
			context['dlms'] = dlms

			## LastDay : Check (dl = False) ##
			try:
				if BFs:
					d_values = BFs
				dd_list = DeadLine_List(dlms, d_values)
				dds = sorted(set(dd_list), key=dd_list.index, reverse=True)
				context['dds'] = dds
			except Exception as e:
				print("Exception - views.py / dl=False / LastDay.Check : %s" % e)

			context['deadlines'] = dl
			## End of LastDay : Check (dl = False) ##

		## name : Setup ##
		#(Def) for name in names:
		#(Def)	context['names'] = name.g_code.name

		name02 = GAS_SpSh_Name(self)
		context['name02'] = name02

		return context


def GAS(request):

	## GAS : JSON - Setup ##
	gJsonFile = "../matsuostationapi-ca6cfa70cc81.json"

	## GAS : SpreadSheet - Setup ##
	spsh_64 = 'SS_#64'
	ws = connect_gspread(gJsonFile, spsh_64)
	ws_list = ws.worksheets()

	## GAS : Read ##
	cell_value = ws_list[0].acell('A1').value

	## GAS : Write ##
	ws_list[0].update_cell(1, 3, cell_value)

	return HttpResponse("A1 = %s" % cell_value)
	# return HttpResponse("GAS.Json.File = %s : %s" % (len(ws_list), ws_list[0].title))
	# return HttpResponse("Hello cFreee/GAS/ You're at the GAS.")


def python(request):

	gJsonFile = "../matsuostationapi-d4eecb8e23c3.json"

	spsh_name = "GooglePython"
	ws = connect_gspread(gJsonFile, spsh_name)
	# spsh_key = "186lVOriJXzl_7wIlLxq7jgAxvrGtCq5YtdprnUpdGi4"
	# ws = connect_gspread(gJsonFile, spsh_key)
	# spsh_url = "https://docs.google.com/spreadsheets/d/186lVOriJXzl_7wIlLxq7jgAxvrGtCq5YtdprnUpdGi4/edit#gid=0"
	# ws = connect_gspread(gJsonFile, spsh_url)
	ws_list = ws.worksheets()


	# ws.update_cell(1,1,"Test_3.92.2")

	return HttpResponse("Google.Json.File = %s : %s , %s" % (len(ws_list), ws_list[0].title, ws_list[1].title) )
	# return HttpResponse("Google.Json.File = %s : %s" % (ws.title, ws.id))
	# return HttpResponse("Hello cFreee/Python You're at the Python.")


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


### Default ###
def index(request):
	return HttpResponse("Hello cFreee/Index.py. You're at the Index.")
