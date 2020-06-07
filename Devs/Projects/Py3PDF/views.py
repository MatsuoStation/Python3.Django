#//+------------------------------------------------------------------+
#//|                      VerysVeryInc.Python3.Django.Py3PDF.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|      "VsV.Py3.Dj.Py3PDF.Views.py - Ver.3.60.5 Update:2020.06.06" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse

### Py3PDF ###
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from glob import glob
import os


''' (Ver.3.60.4)
import sys
import os
from pathlib import Path
from subprocess import call
'''


### Test ###
def Test(request):
	# return HttpResponse("Test.Py3PDF.API Page!! Welcome to Devs.MatsuoStation.Com!")

	scan_pdf_path = os.path.join(os.path.dirname(os.getcwd()), 'Devs', 'ScanPDF')
	file_list = glob(str(scan_pdf_path)+'/20200606151704_x.pdf')
	txt_file = str(scan_pdf_path)+'/pdf.txt'

	result_list = []

	for item in file_list:
		result_txt = Convert_PDF_to_Txt(item)
		result_list.append(result_txt)

	AllText= ','.join(result_list)	# PDF毎のテキストが配列に格納さてているので、連結

	fp = open(str(scan_pdf_path)+'/pdf.txt', 'w')	# FILE OPEN : 書き込みモード
	fp.write(AllText)
	fp.close()

	return HttpResponse(txt_file)


	''' (Ver.3.60.4)
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
	'''

### Convert_PDF_to_Txt ###
def Convert_PDF_to_Txt(path):
	RsrcMgr = PDFResourceManager()
	RetStr	= StringIO()
	codec = 'utf-8'

	laparams = LAParams()
	laparams.detect_vertical = True		## Trueにすることで、綺麗にテキストを抽出できる

	device = TextConverter(RsrcMgr, RetStr, codec=codec, laparams=laparams)

	## File : OPEN
	fp = open(path, 'rb')

	interpreter = PDFPageInterpreter(RsrcMgr, device)
	maxpages = 0
	caching = True
	pagenos=set()
	fstr = ''

	for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching= caching, check_extractable=True):
		interpreter.process_page(page)

		str = RetStr.getvalue()
		fstr += str

	fp.close()
	device.close()
	RetStr.close()

	return fstr


### Index ###
def index(request):
	return HttpResponse("Hello Py3PDF.py. You're at the Index.")
