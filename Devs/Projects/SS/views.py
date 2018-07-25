#//+------------------------------------------------------------------+
#//|                          VerysVeryInc.Python3.Django.SS.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Django.LPG.Views.py - Ver.3.12.3 Update:2018.07.24" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import ListView
from .forms import DateForm

from Finance.models import InCash_Test20

### SS_Incash ###
class SS_InCash(ListView):

	model = InCash_Test20
	form_class = DateForm
	template_name = 'ss_incash.html'
	context_object_name = "incashtb"
	paginate_by = 120

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		md_post = request.POST['md']
		if form.is_valid():
			return HttpResponseRedirect('/SS/?dl=%s' % md_post)

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		contex = super().get_context_data(**kwargs)

		return contex


### Index ###
def index(request):
	# return HttpResponse("Devs.SS Page!! Welcome to Devs.MatsuoStation.Com!")
	if request.method == 'POST':
		form = DateForm(request.POST)
		md_post = request.POST['md']
		if form.is_valid():
			return HttpResponseRedirect('/SS/?dl=%s' % md_post)

	else:
		form = DateForm()

	return render(request, 'ss_incash.html', {'form': form})
