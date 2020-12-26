#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.vInvoice.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|    "VsV.Py3.Dj.vInvoice.Views.py - Ver.3.80.4 Update:2020.12.26" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView

from .forms import NameForm
from Finance.models import Invoice_Test20, Name_Test20


### vInvoice_List ###
class vInvoice_List(ListView):
	model = Name_Test20
	form_class = NameForm
	template_name = 'vlist.html'
	context_object_name = "nametb"
	paginate_by = 30

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post )
		return render(request, self.template_name, {'form': form})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		### Search : g_code ###
		context['form'] = NameForm()
		context['gid'] = self.kwargs.get('nid')

		### DB : Setup ###
		names = Invoice_Test20.objects.filter(g_code__uid=self.kwargs.get('nid')).select_related('g_code')

		for name in names:
			context['names'] = name.g_code.name

		return context


def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		nid_post = request.POST['nid']
		if form.is_valid():
			return HttpResponseRedirect('/vInvoice/%s' % nid_post)
	else:
		form = NameForm()
	return render(request, 'vInvoice.html', {'form': form})

	# return HttpResponse("Hello vInvoice/view.py. You're at the vInvoice.")
