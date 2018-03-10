#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.Finance.Models.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Dj.Finance.Models.py - Ver.3.3.1 Update:2018.03.10" |
#//+------------------------------------------------------------------+
from django.db import models

# Create your models here.
### MatsuoStation.Com ###
###* ScanXLS *###
class ScanXLS_Test(models.Model):
	class Meta:
		db_table = 'ScanXLS_Test'
		verbose_name = 'ScanPos_000'
		verbose_name_plural = verbose_name
		ordering = ['-day']

	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	day		= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_type	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	car_code= models.CharField( verbose_name='顧客車番', default=None, max_length=4 )
	memo	= models.CharField( verbose_name='メモ', default=None, max_length=3 )
	pw_code	= models.CharField( verbose_name='暗証番号', default=None, max_length=4 )
	exp_day	= models.CharField( verbose_name='有効期限', default=None, max_length=6 )
	staff	= models.CharField( verbose_name='担当コード', default=None, max_length=3 )
	red_code= models.IntegerField( verbose_name='赤伝', default=0 )						# max_length=1,
	slip	= models.CharField( verbose_name='伝票番号', default=None, max_length=4 )
	pump	= models.CharField( verbose_name='ポンプ番号', default=None, max_length=3 )
	nozzle	= models.IntegerField( verbose_name='ノズル番号', default=0 )					# max_length=1,
	pro_memo= models.CharField( verbose_name='商品メモ', default=None, max_length=11 )
	product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	amount	= models.IntegerField( verbose_name='数量', default=0 )						# max_length=8,
	unit	= models.IntegerField( verbose_name='単価', default=0 )						# max_length=8,
	value	= models.IntegerField( verbose_name='税別金額', default=0 )					# max_length=9,
	# tax_code= models.IntegerField( verbose_name='税区分', default=0 )					# max_length=1,
