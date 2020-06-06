#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.Py3PDF.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Py3PDF.Views.py - Ver.3.60.4 Update:2020.06.06" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

### Py3PDF ###
import sys
import os
from pathlib import Path
from subprocess import call



def Test(request):
	# return HttpResponse("Test.Py3PDF.API Page!! Welcome to Devs.MatsuoStation.Com!")

	### pdf2txt.py : PATH
	py_path = Path(sys.exec_prefix) / "bin" / "pdf2txt.py"
	# return HttpResponse(py_path)

	### pdf2txt.py : CALL
	Main_Dir = os.getcwd()
	scan_pdf_path = os.path.join(os.path.dirname(Main_Dir), 'Devs', 'ScanPDF')
	# scan_pdf_path = Path(sys.exec_prefix)
	# (OK) call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/simple1.pdf"])
	# call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/2020-06-06-09-50-00.pdf"])
	# call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/extract-sample.pdf"])
	# call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/20200606151704.pdf"])
	# call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/20200606151704_a.pdf"])
	call([str(py_path), "-o" , str(scan_pdf_path)+"/simple1.txt", "-p 1", str(scan_pdf_path)+"/20200607073702_x.pdf"])

	return HttpResponse(Main_Dir)





def index(request):
	return HttpResponse("Hello Py3PDF.py. You're at the Index.")
