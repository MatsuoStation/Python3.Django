from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
	return HttpResponse("Devs.SS Page!! Welcome to Devs.MatsuoStation.Com!")
