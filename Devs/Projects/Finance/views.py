#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Finance.Views.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Finance.Views.py - Ver.3.7.1 Update:2018.03.25" |
#//+------------------------------------------------------------------+
from django.shortcuts import render

# Create your views here.
### MatsuoStation.Com ###
from django.http import HttpResponse
import re
import numpy as np


def index(request):
	return HttpResponse("Finance Page!! Welcome to Devs.MatsuoStation.Com!")

### 93.92.91 : Delete ###



### SHARP ###
def GoLast_g_code(line):
	# return re.sub('(^([^,]*,){7})(.{5})(.*)', '\\1\\4,\\3', line, flags=re.MULTILINE)
	return re.sub('(^([^,]*,){6})(.{5})(.*)', '\\1\\4,\\3', line, flags=re.MULTILINE)

def GoLast_s_code(line):
	# return re.sub('(^([^,]*,){17})(.{6})(.*)', '\\1\\4,\\3', line, flags=re.MULTILINE)
	return re.sub('(^([^,]*,){16})(.{6})(.*)', '\\1\\4,\\3', line, flags=re.MULTILINE)


### ALL ###
def Start4(line):
	return re.sub('(^.{4})', '\\1,', line, flags=re.MULTILINE)
	# return re.sub('(^.{%s})' % value, '\\1,', line, flags=re.MULTILINE)

def Start2(line):
	return re.sub('(,)(.{2})', '\\1\\2,', line, flags=re.MULTILINE)
	# return re.sub('(^.{%s})' % value, '\\1,', line, flags=re.MULTILINE)

def Comma( line, value ):
	return re.sub('(^.*,)(.{%s})' % value, '\\1\\2,', line, flags=re.MULTILINE)
	# return re.sub('(^.*,)(.{1})', '\\1\\2,', line, flags=re.MULTILINE)

def LastCommaDel(line):
	return re.sub('(.{0},$)', '', line, flags=re.MULTILINE)

def CalDel(line):
	return re.sub('(.{9}$)', '', line, flags=re.MULTILINE)

#def DayMove(line):
#	return re.sub('(^.{5})(.*,)(.{8}$)', '\\1\\3,\\2', line, flags=re.MULTILINE)
def DayBar(line):
	return re.sub('(.{4})(.{2})(.{2}$)', '\\1/\\2/\\3', line, flags=re.MULTILINE)

# def TimeMove(line):
#	return re.sub('(^.{14})(.*,)(.{4})', '\\1\\3,\\2', line, flags=re.MULTILINE)
def TimeColon(line):
	return re.sub('(.{11}$)', ':\\1', line, flags=re.MULTILINE)

def DayTimeMerge(line):
	return re.sub('(.*,)(.{6})(.{10}$)', '\\1\\3 \\2', line, flags=re.MULTILINE)
def DayTimeMove(line):
	return re.sub('(^.{5})(.*,)(.{16}$)', '\\1\\3,\\2', line, flags=re.MULTILINE)


def Del5(line):
	# return re.sub('(^([^,]*,){29})(.{13})(.*)', '\\1\\4', line, flags=re.MULTILINE)
	return re.sub('(^([^,]*,){27})(.{16})(.*)', '\\1\\4', line, flags=re.MULTILINE)

def Del7(line):
	# return re.sub('(^([^,]*,){32})(.{65})(.*)', '\\1\\4', line, flags=re.MULTILINE)
	return re.sub('(^([^,]*,){30})(.{46})(.*)', '\\1\\4', line, flags=re.MULTILINE)

def DelEn(line):
	return re.sub('^\n', '', line, flags=re.MULTILINE)


def sharp(request):
# def mysql(request):
# def mysql_00(request):

	csvfile = "PosData/20180228.csv"
	SHARP_ALL(csvfile)
	csvfile_out = "PosData/20180228_11.csv"

	pData = np.genfromtxt(csvfile_out, delimiter=",", skip_header=0, dtype='str')
	# posdata = np.loadtxt(csvfile_out, delimiter=',', skiprows=0, fmt="%.5f")
	# data = np.genfromtxt(csvfile_out, delimiter=',', skiprows=0)

	# FinalCheck : Delete - 93 & 92 & 91
	FCrows, FCcols = np.where( (pData == '91') | (pData == '92') | (pData=='93') )
	pData = np.delete( pData, FCrows[ np.where(FCcols==2) ], 0 )

	# InvoiceList(売掛リスト) : 9
	# (OK) IVrows, IVcols = np.where( (pData != '9') )
	# (OK) pData = np.delete( pData, IVrows[ np.where(IVcols==5) ], 0 )

	# np.savetxt("PosData/20180228_06.csv", posdata, delimiter=',', fmt='%.4f')
	np.savetxt("SHARP/20180228_22.csv", pData, delimiter=',', fmt='%s')

	return HttpResponse("New.MySQL.OK! rows=%s, cols=%s " % (FCrows,FCcols) )
	# (OK) return HttpResponse("New.MySQL.OK! rows=%s, cols=%s " % (IVrows,IVcols) )
	# return HttpResponse("New.MySQL.OK! rows=%s, cols=%s " % (FCrows,FCcols) )
	# return HttpResponse("New.MySQL.OK! %s " % pData)


def SHARP_ALL(csvfile):
# def mysql(request):
	# return HttpResponse("Finance MySQL Page!! Welcome to MySQL.Devs.MatsuoStation.Com!")

	# (OK) file = open("PosData/20180228.csv", "r")
	# out_file = open("PosData/20180228_04.csv", "w")

	file = open(csvfile, "r")
	out_file = open("PosData/20180228_11.csv", "w")

	# file.readline()			# Delete : First Line
	lines = file.readlines()

	for line in lines:
		# HH_Del
		# line = line.replace("(HH)(.{258})", "")

		### SHARP.POS ###
		### ALL ###
		line = re.sub('(HH)(.{258})', "\n", line)
		line = re.sub('D0PH', "\n", line)

		# line = re.sub('(.{8}$)', "", line, flags=re.MULTILINE)
		# ( SEQ番号 - 処理区分 - データ種別 )
		line = Start4(line)
		line = Start2(line)
		line = Comma(line,3)
		# line = Start4(line)
		# line = re.sub('(^.{4})', '\\1,', line, flags=re.MULTILINE)

		# ( 決済コード　- SSコード - 顧客コード - 車番 - メモ )
		line = Comma(line,1)
		line = Comma(line,5)
		line = Comma(line,4)
		line = Comma(line,4)
		line = Comma(line,3)

		# ( 車番 - 有効年月日 - 担当コード　)
		line = Comma(line,4)
		line = Comma(line,6)
		line = Comma(line,3)

		# ( 赤伝 - 伝票No. - ポンプNo. - ノズルNo. - <商品メモ> )
		line = Comma(line,1)
		line = Comma(line,4)
		line = Comma(line,3)
		line = Comma(line,1)
		line = Comma(line,11)

		# ( <商品> - <数量(6.2)> - <単価(7.1)> - <税別金額> )
		line = Comma(line,5)
		line = Comma(line,8)	# 数量:Float対応
		line = Comma(line,8)
		line = Comma(line,9)

		# ( <税区別> - <消費税> - <軽油税>  )
		line = Comma(line,1)
		line = Comma(line,9)
		line = Comma(line,9)

		# ( ポイント - 支払い区分 - 承認No. - 割賦回数 )
		line = Comma(line,7)
		line = Comma(line,1)
		line = Comma(line,10)
		line = Comma(line,2)

		# ( ペイパス - ID - 業態 - 企業コード - ネガ/オーソリFG )
		line = Comma(line,1)
		line = Comma(line,1)
		line = Comma(line,1)
		line = Comma(line,4)
		line = Comma(line,1)

		# ( クーポン値引区分 - 値引単価 - 値引金額 )
		line = Comma(line,1)
		line = Comma(line,5)
		line = Comma(line,6)

		# ( 仕向先コード - 標準商品コード )
		line = Comma(line,2)
		line = Comma(line,5)

		# // ( 忠VISA用車番 - 忠併用区分 - 忠会員コード - 忠VISA時顧客番号(特約店コード) )
		line = Comma(line,5)
		line = Comma(line,1)
		line = Comma(line,17)
		line = Comma(line,10)

		# ( 客先名 )
		line = Comma(line,18)

		# ( 伝票年月日(修正) - 伝票No.(修正) - サブデータ(修正:6.2) )
		line = Comma(line,8)
		line = Comma(line,4)
		line = Comma(line,8)

		# ( SSコード(処理) - 時分(処理) - 伝票年月日(処理) - カレンダー年月日(処理) )
		line = Comma(line,10)
		line = Comma(line,4)
		line = Comma(line,8)
		# line = Comma(line,8)

		# システムカレンダー削除
		line = CalDel(line)

		# 時分(処理) : コロン
		line = TimeColon(line)
		# 伝票年月日(処理)  : /
		line = DayBar(line)

		# 伝票年月日(処理) - 時分(処理) : 結合
		line = DayTimeMerge(line)
		line = LastCommaDel(line)
		# 伝票年月日(処理) - 時分(処理) : 移動
		line = DayTimeMove(line)
		line = LastCommaDel(line)

		### OLD ###
		# 伝票年月日(処理) - 時分(処理) : 移動
		# line = DayMove(line)
		# line = LastCommaDel(line)
		# line = TimeMove(line)
		# line = LastCommaDel(line)
		### End of OLD ###

		# ( ペイパス - ID - 業態 - 企業コード - ネガ/オーソリFG : 削除 )
		line = Del5(line)

		# ( 仕向先コード - 標準商品コード : 削除 )
		# ( 忠VISA用車番 - 忠併用区分 - 忠会員コード - 忠VISA時顧客番号(特約店コード)　: 削除 )
		line = Del7(line)

		# (空行削除)
		line = DelEn(line)
		### End of ALL ###

		### SHARP ###
		# g_code : 後退
		line = GoLast_g_code(line)
		line = LastCommaDel(line)

		# s_code : 後退
		line = GoLast_s_code(line)
		line = LastCommaDel(line)

		### End of SHARP ###

		out_file.write(line)

	file.close()
	out_file.close()

	# (Def.OK) return HttpResponse("MySQL.OK!")
