#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.aInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.aInvoice.Views.py - Ver.3.90.2 Update:2021.01.14" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm

### Index(request) ###
def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/aInvoice/%s' % nid_post)
	else:
		form = NameForm()
	return render(request, 'aInvoice.html', {'form': form})

	# return HttpResponse("Hello aInvoice/view.py. You're at the aInvoice.")