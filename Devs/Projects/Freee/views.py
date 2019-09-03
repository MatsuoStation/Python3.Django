#//+------------------------------------------------------------------+
#//|                       VerysVeryInc.Python3.Django.Index.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|       "VsV.Py3.Dj.Freee.Views.py - Ver.3.20.9 Update:2019.09.03" |
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

import pymysql.cursors

from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger


### DictFetchAll ###
def dictfetchall(cursor):
	# "Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

### Uriage_List ###
class Uriage_List(ListView):

	model = Name_Test20
	form_class = YearForm
	template_name = 'uriage_list.html'
	context_object_name = "nametb"
	# paginate_by = 5

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
		SHARP20_K = 'SHARP20_K_' + str(yid)
		context['SHARP20_K'] = SHARP20_K

		### MySQL:Connection ###
		conn = pymysql.connect(read_default_file='../../ssh/AWS_RDS_Dev.cnf')

		try:
			### MySQL:Session ###
			with conn.cursor() as cursor:
				# sql = "SELECT * FROM SHARP20_K_2019 WHERE m_datetime < %s AND p_code = %s AND r_code IN (%s,%s)  ORDER BY m_datetime"
				# sql = "SELECT * FROM %s " % SHARP20_K + "WHERE m_datetime < %s AND p_code = %s AND r_code IN (%s,%s)  ORDER BY m_datetime"
				sql = "SELECT * FROM %s " % SHARP20_K + "WHERE p_code = %s AND r_code IN (%s,%s)  ORDER BY m_datetime"
				# cursor.execute(sql,("2018-07-03","10","0","1",))
				# cursor.execute(sql,("2018-07-03","10","0","1",))
				cursor.execute(sql,("10","0","1",))

				SQL_Data = dictfetchall(cursor)
				# context['sqls'] = SQL_Data

				# result = cursor.fetchall()
				# print(result)
				# context['sqls'] = result

		finally:
			conn.close()

		### Pager ###
		paginator = Paginator(SQL_Data, 5)
		try:
			page = int(self.request.GET.get('page'))
		except:
			page = 1

		try:
			SQL_Data = paginator.page(page)
		except(EmptyPage, InvalidPage):
			SQL_Data = paginator.page(1)


		context['sqls'] = SQL_Data

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


### Index ###
def index(request):
	return HttpResponse("Hello Freee.Py3 You're at the Index.")
