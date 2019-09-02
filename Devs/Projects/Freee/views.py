#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|       "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.5 Update:2019.09.02" |
#//+------------------------------------------------------------------+
# rom django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
# from django.http import HttpResponse

from django.views.generic import ListView
from Finance.models import Name_Test20
from .forms import YearForm

### Uriage_List ###
class Uriage_List(ListView):

	model = Name_Test20
	form_class = YearForm
	template_name = 'uriage_list.html'
	context_object_name = "nametb"
	paginate_by = 10

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		yid_post = request.POST['yid']

		if form.is_valid():
			return HttpResponseRedirect( '/Freee/Uriage/%s' % yid_post )

		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['form'] = YearForm()
		yid = self.kwargs.get('yid')
		context['yid'] = yid

		return context


### Uriage ###
def Uriage(request):
	# return HttpResponse("Hello Uriage.Py3 You're at the Uriage.")

	if request.method == 'POST':
		form = YearForm(request.POST)
		yid_post = request.POST['yid']
		if form.is_valid():
			return HttpResponseRedirect('/Freee/Uriage/%s' % yid_post)

	else:
		form = YearForm()

	return render(request, 'uriage.html', {'form': form})


def index(request):
	return HttpResponse("Hello Freee.Py3 You're at the Index.")
