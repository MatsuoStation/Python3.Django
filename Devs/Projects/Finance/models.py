#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.Finance.Models.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//| "VsV.Python3.Dj.Finance.Models.py - Ver.3.3.5 Update:2018.03.12" |
#//+------------------------------------------------------------------+
from django.db import models

# Create your models here.
### MatsuoStation.Com ###
###* Guest.Address *###
class Add_Test(models.Model):
	class Meta:
		db_table = 'Address_Test'
		verbose_name = 'Address_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	postal_code = models.CharField( "郵便番号", default=None, max_length=16 )
	address = models.CharField( "住所", default=None, max_length=255 )


###* Guest.Bank *###
class Bank_Test(models.Model):
	class Meta:
		db_table = 'Bank_Test'
		verbose_name = 'Bank_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	bank_name = models.CharField( "銀行名", default=None, max_length=255 )
	bank_number = models.IntegerField( "銀行番号", default=0 )
	branch_number = models.IntegerField( "支店番号", default=0 )
	account_kind = models.CharField( "口座種類", default=None, max_length=255 )
	account = models.CharField( "口座番号", default=None, max_length=255 )
	check = models.IntegerField( "締切日", default=0 )
	receipt = models.IntegerField( "領収書添付有無", default=0 )


###* Guest.Name *###
class Name_Test(models.Model):
	class Meta:
		db_table = 'Name_Test'
		verbose_name = 'Name_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	name_furigana = models.CharField( "顧客フリガナ", default=None, max_length=255 )

###* SHARP *###
class SHARP_Test(models.Model):
	class Meta:
		db_table = 'SHARP_Test'
		verbose_name = 'SHARP_000'
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
	tax_code= models.IntegerField( verbose_name='税区分', default=0 )					# max_length=1,
	tax 	= models.IntegerField( verbose_name='消費税', default=0 )					# max_length=9,
	oil_tax	= models.IntegerField( verbose_name='軽油税', default=0 )					# max_length=9,
	point	= models.IntegerField( verbose_name='ポイント', default=0 )					# max_length=7,
	pay_code= models.IntegerField( verbose_name='支払区分', default=0 )					# max_length=1,
	auth_no	= models.CharField( verbose_name='承認No', default=None, max_length=10 )
	allot	= models.IntegerField( verbose_name='割賦回数', default=0 )					# max_length=2,
	coupon	= models.IntegerField( verbose_name='クーポン割引区分', default=0 )			# max_length=1,
	dis_unit= models.IntegerField( verbose_name='割引単価', default=0 )					# max_length=5,
	d_value	= models.IntegerField( verbose_name='割引金額', default=0 )					# max_length=6,
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )


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
