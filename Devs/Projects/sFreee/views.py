#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.sFreee.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.sFreee.Views.py - Ver.3.93.7 Update:2021.08.28" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from .forms import DateForm

### Google.API ###
from .Util.Connect_GSpread import connect_gspread

### MySQL ###
from Finance.models import SHARPnPOS_1501_2107
from datetime import datetime, timedelta
from .Util.deadline import DeadLine

### Google Apps Script ###
class GAS(ListView):
	model = SHARPnPOS_1501_2107
	form_class = DateForm
	# model = Name_Test20
	# form_class = NameForm
	template_name = 'sFreeeList.html'

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		mdate_post = request.POST['mdate']
		if form.is_valid():
			return HttpResponseRedirect('/sFreee/GAS/%s' % mdate_post)
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		## GAS : SpreadSheet - Setup ##
		spsh_name = "SS_U"
		ws = connect_gspread(spsh_name)
		ws_list = ws.worksheets()

		## Search : m_datetime ##
		context['form'] = DateForm()
		if self.kwargs.get('mdate'):
			mdate = self.kwargs.get('mdate')
		else:
			mdate = '2000-01'

		## * try: * dl = Ture ##
		try:
			dl = mdate + '-01'
			dlstr = datetime.strptime(dl, '%Y-%m-%d')

			# dd = dlstr.day  # DeadLine : Day
			dlb, dla = DeadLine(dlstr)
			# dld, dlm, dlb, dla, bld, blm = DeadLine(dd, dlstr)

		## * end try: * dl = False ##
		except Exception as e:
			print("Exception - views.py / dl=False  : %s" % e)

		context['mdate'] = mdate
		context['dlb'] = dlb
		context['dla'] = dla


		## GAS : シート追加
		''' (OK)
		newShName = dl.replace('20', '').replace('-', '')
		ws_list_value = 0

		for i in range(len(ws_list)):
			# context['ws_list_len'] = len(ws_list)
			# context['ws_list_name'] = ws_list[i].title
			if (ws_list[i].title == newShName):
				ws_list_value = ws_list_value + 1
		ws_list_cpid = ws_list[0].id
		# context['ws_list_cpid'] = ws_list_cpid

		if ws_list_value == 0:
			ws.duplicate_sheet(source_sheet_id=ws_list_cpid, new_sheet_name=newShName, insert_sheet_index=len(ws_list))
			# ws.add_worksheet(title=newShName, rows=100, cols=25)
		# context['ws_list_vl'] = ws_list_value
		'''

		return context


def GAS_Def(request):
	## GAS : SpreadSheet - Setup ##
	spsh_name = "SS_U"
	# spsh_name = "GooglePython"

	ws = connect_gspread(spsh_name)
	# ws = connect_gspread(gJsonFile, spsh_name)
	ws_list = ws.worksheets()

	## GAS : Read ##
	cell_value = ws_list[0].acell('A1').value

	## GAS : Write ##
	ws_list[0].update_cell(1, 18, cell_value)

	return HttpResponse("A1 = %s" % cell_value)
	# return HttpResponse("SS_U.Json.File = %s : %s" % (len(ws_list), ws_list[0].title))
	# return HttpResponse("Google.Json.File = %s : %s , %s" % (len(ws_list), ws_list[0].title, ws_list[1].title))
	# return HttpResponse("Hello sFreee/GAS/ You're at the Google Apps Script.")

### Default ###
def index(request):
	return HttpResponse("Hello RDS to CSV sFreee/Index.py. You're at the Index.")
