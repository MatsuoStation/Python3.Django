#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.Finance.Models.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.Finance.Models.py - Ver.3.11.11 Update:2018.05.24" |
#//+------------------------------------------------------------------+
from django.db import models

# Create your models here.
### MatsuoStation.Com ###
from django.conf import settings


# settings.DATETIME_FORMAT

###* LPG.Meter00 *### (uid : IntegerField)
class LPG_Meter00(models.Model):
	class Meta:
		db_table = 'LPG_Meter00'
		verbose_name = 'LPT_Meter_020'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	route_code  = models.IntegerField( "ルート順番", default=None )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	m_datetime 	= models.DateTimeField( verbose_name='検針日' )
	meter	= models.FloatField( "検針値", default=None )
	amount	= models.FloatField( "使用量", default=None )
	date01 	= models.DateTimeField( verbose_name='検針日01' )
	meter01	= models.FloatField( "検針値01", default=None )
	amount01= models.FloatField( "使用量01", default=None )
	date02 	= models.DateTimeField( verbose_name='検針日02' )
	meter02	= models.FloatField( "検針値02", default=None )
	amount02= models.FloatField( "使用量02", default=None )
	date03 	= models.DateTimeField( verbose_name='検針日03' )
	meter03	= models.FloatField( "検針値03", default=None )
	amount03= models.FloatField( "使用量03", default=None )
	date04 	= models.DateTimeField( verbose_name='検針日04' )
	meter04	= models.FloatField( "検針値04", default=None )
	amount04= models.FloatField( "使用量04", default=None )
	date05 	= models.DateTimeField( verbose_name='検針日05' )
	meter05	= models.FloatField( "検針値05", default=None )
	amount05= models.FloatField( "使用量05", default=None )
	date06 	= models.DateTimeField( verbose_name='検針日06' )
	meter06	= models.FloatField( "検針値06", default=None )
	amount06= models.FloatField( "使用量06", default=None )
	date07 	= models.DateTimeField( verbose_name='検針日07' )
	meter07	= models.FloatField( "検針値07", default=None )
	amount07= models.FloatField( "使用量07", default=None )
	date08 	= models.DateTimeField( verbose_name='検針日08' )
	meter08	= models.FloatField( "検針値08", default=None )
	amount08= models.FloatField( "使用量08", default=None )
	date09 	= models.DateTimeField( verbose_name='検針日09' )
	meter09	= models.FloatField( "検針値09", default=None )
	amount09= models.FloatField( "使用量09", default=None )
	date10 	= models.DateTimeField( verbose_name='検針日10' )
	meter10	= models.FloatField( "検針値10", default=None )
	amount10= models.FloatField( "使用量10", default=None )
	date11 	= models.DateTimeField( verbose_name='検針日11' )
	meter11	= models.FloatField( "検針値11", default=None )
	amount11= models.FloatField( "使用量11", default=None )
	date12 	= models.DateTimeField( verbose_name='検針日12' )
	meter12	= models.FloatField( "検針値12", default=None )
	amount12= models.FloatField( "使用量12", default=None )

	def __str__(self):
		return self.uid


###* LPG.Value00 *### (uid : IntegerField)
class LPG_Value00(models.Model):
	class Meta:
		db_table = 'LPG_Value00'
		verbose_name = 'LPT_Value_020'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None )
	base_value	= models.IntegerField( verbose_name='基本料金(税別)', default=0 )
	start_value	= models.FloatField( "初期数量", default=None )
	end_value	= models.FloatField( "上限数量", default=None )
	unit    	= models.FloatField( "単価", default=None )

	def __str__(self):
		return self.uid


###* Tutorial.Dj2.0 *###
'''
class Question(models.Model):
	class Meta:
		db_table = 'Question_Test'
		verbose_name = 'Question_000'
		verbose_name_plural = verbose_name
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=4 )
	question_text = models.CharField('問題', max_length=200)
	pub_date = models.DateTimeField('date published')

class Choice(models.Model):
	class Meta:
		db_table = 'Choice_Test'
		verbose_name = 'Choice_000'
		verbose_name_plural = verbose_name
	question = models.ForeignKey(Question, related_name='question_uid', on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
'''

###* Tools.Items *###
class Items_Test(models.Model):
	class Meta:
		db_table = 'Items_Test'
		verbose_name = 'Items_000'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=4 )
	hinmoku = models.CharField( "種別", default=None, max_length=255 )
	h_name = models.CharField( "品目名", default=None, max_length=255 )
	sc1 = models.CharField( "ショートカット1", default=None, max_length=255 )
	sc2 = models.CharField( "ショートカット2", default=None, max_length=255 )
	name = models.CharField( "正式名称", default=None, max_length=255 )

	def __str__(self):
		return self.uid



###* Guest.Discount *###
class Discount_Test(models.Model):
	class Meta:
		db_table = 'Discount_Test'
		verbose_name = 'Discount_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	car_code= models.CharField( verbose_name='顧客車番', default=None, max_length=4 )
	lastday	= models.PositiveIntegerField( "終了期日", default=None )
	value	= models.FloatField( "価格", default=None )

	def __str__(self):
		return self.uid


###* Guest.Value *###
class Value_Test(models.Model):
	class Meta:
		db_table = 'Value_Test'
		verbose_name = 'Value_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	day		= models.PositiveIntegerField( "設定日", default=None )
	value	= models.FloatField( "価格", default=None )
	date01	= models.PositiveIntegerField( "設定日01", default=None )
	value01	= models.FloatField( "価格01", default=None )
	date02	= models.PositiveIntegerField( "設定日02", default=None )
	value02	= models.FloatField( "価格02", default=None )
	date03	= models.PositiveIntegerField( "設定日03", default=None )
	value03	= models.FloatField( "価格03", default=None )

	def __str__(self):
		return self.uid


###* Guest.Value10 *###
class Value_Test10(models.Model):
	class Meta:
		db_table = 'Value_Test10'
		verbose_name = 'Value_010'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# day		= models.PositiveIntegerField( "設定日", default=None )
	m_datetime 	= models.DateTimeField( verbose_name='設定日' )
	value	= models.FloatField( "価格", default=None )
	date01	= models.DateTimeField( "設定日01")
	value01	= models.FloatField( "価格01", default=None )
	date02	= models.DateTimeField( "設定日02")
	value02	= models.FloatField( "価格02", default=None )
	date03	= models.DateTimeField( "設定日03")
	value03	= models.FloatField( "価格03", default=None )

	def __str__(self):
		return self.uid


###* Guest.Value20 *### (uid : IntegerField)
class Value_Test20(models.Model):
	class Meta:
		db_table = 'Value_Test20'
		verbose_name = 'Value_020'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	tax_code= models.IntegerField( verbose_name='税区分', default=0 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# day		= models.PositiveIntegerField( "設定日", default=None )
	m_datetime 	= models.DateTimeField( verbose_name='設定日' )
	value	= models.FloatField( "価格", default=None )
	date01	= models.DateTimeField( "設定日01")
	value01	= models.FloatField( "価格01", default=None )
	date02	= models.DateTimeField( "設定日02")
	value02	= models.FloatField( "価格02", default=None )
	date03	= models.DateTimeField( "設定日03")
	value03	= models.FloatField( "価格03", default=None )

	def __str__(self):
		return self.uid


###* Guest.Value30 *### (uid : IntegerField)
class Value_Test30(models.Model):
	class Meta:
		db_table = 'Value_Test30'
		verbose_name = 'Value_030'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	lpg_code= models.IntegerField( verbose_name='ガス料金コード', default=0 )
	tax_code= models.IntegerField( verbose_name='税区分', default=0 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# day		= models.PositiveIntegerField( "設定日", default=None )
	m_datetime 	= models.DateTimeField( verbose_name='設定日' )
	value	= models.FloatField( "価格", default=None )
	date01	= models.DateTimeField( "設定日01")
	value01	= models.FloatField( "価格01", default=None )
	date02	= models.DateTimeField( "設定日02")
	value02	= models.FloatField( "価格02", default=None )
	date03	= models.DateTimeField( "設定日03")
	value03	= models.FloatField( "価格03", default=None )
	date04	= models.DateTimeField( "設定日04")
	value04	= models.FloatField( "価格04", default=None )
	date05	= models.DateTimeField( "設定日05")
	value05	= models.FloatField( "価格05", default=None )
	date06	= models.DateTimeField( "設定日06")
	value06	= models.FloatField( "価格06", default=None )
	date07	= models.DateTimeField( "設定日07")
	value07	= models.FloatField( "価格07", default=None )
	date08	= models.DateTimeField( "設定日08")
	value08	= models.FloatField( "価格08", default=None )
	date09	= models.DateTimeField( "設定日09")
	value09	= models.FloatField( "価格09", default=None )
	date10	= models.DateTimeField( "設定日10")
	value10	= models.FloatField( "価格10", default=None )
	date11	= models.DateTimeField( "設定日11")
	value11	= models.FloatField( "価格11", default=None )
	date12	= models.DateTimeField( "設定日12")
	value12	= models.FloatField( "価格12", default=None )

	def __str__(self):
		return self.uid


###* Guest.Tel *###
class Tel_Test(models.Model):
	class Meta:
		db_table = 'Tel_Test'
		verbose_name = 'Tel_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	phone = models.CharField( "電話番号", default=None, max_length=16 )
	mobile_tel = models.CharField( "携帯電話", default=None, max_length=16 )

	def __str__(self):
		return self.uid


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

	def __str__(self):
		return self.uid


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
	# bank_number = models.CharField( "銀行番号", default=None, max_length=255 )
	bank_number = models.PositiveSmallIntegerField( "銀行番号", default=None)
	# branch_number = models.IntegerField( "支店番号", default=0 )
	branch_number = models.PositiveSmallIntegerField( "支店番号", default=None )
	account_kind = models.CharField( "口座種類", default=None, max_length=255 )
	# account = models.CharField( "口座番号", default=None, max_length=255 )
	account = models.PositiveIntegerField( "口座番号", default=None )
	# check = models.IntegerField( "締切日", default=0 )
	check_day = models.PositiveSmallIntegerField( "締切日", default=None )
	# receipt = models.IntegerField( "領収書添付有無", default=0 )
	receipt = models.PositiveSmallIntegerField( "領収書添付有無", default=None )
	s_format = models.PositiveSmallIntegerField( "請求書フォーマット", default=None )
	r_code	= models.IntegerField( verbose_name='掛現金/掛振込', default=0 )

	def __str__(self):
		return self.uid


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

	def __str__(self):
		return self.uid


###* SHARP *###
class SHARP_Test(models.Model):
	class Meta:
		db_table = 'SHARP_Test'
		verbose_name = 'SHARP_000'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
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

	def __str__(self):
		return self.g_code


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




###* Guest.Name.002 *### ( uid : unique )
class Name_Test02(models.Model):
	class Meta:
		db_table = 'Name_Test02'
		verbose_name = 'Name_002'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	# id = models.AutoField( "id", primary_key=True )
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16, unique=True )
	# uid  = models.CharField( "共通ID", default=None, unique=True, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	name_furigana = models.CharField( "顧客フリガナ", default=None, max_length=255 )

	def __str__(self):
		return self.uid

###* SHARP.002 *### (g_code:ForeignKey)
class SHARP_Test02(models.Model):
	class Meta:
		db_table = 'SHARP_Test02'
		verbose_name = 'SHARP_002'
		verbose_name_plural = verbose_name
		ordering = ['m_day']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp02', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.g_code



###* Tools.Items02 *### (uid.unique)
class Items_Test02(models.Model):
	class Meta:
		db_table = 'Items_Test02'
		verbose_name = 'Items_002'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=5, unique=True )
	hinmoku = models.CharField( "種別", default=None, max_length=255 )
	h_name = models.CharField( "品目名", default=None, max_length=255 )
	sc1 = models.CharField( "ショートカット1", default=None, max_length=255 )
	sc2 = models.CharField( "ショートカット2", default=None, max_length=255 )
	name = models.CharField( "正式名称", default=None, max_length=255 )

	def __str__(self):
		return self.uid



###* SHARP.003 *### (g_code:OneToOneField)
class SHARP_Test03(models.Model):
	class Meta:
		db_table = 'SHARP_Test03'
		verbose_name = 'SHARP_003'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test02',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='sharp03',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test02',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='sharp03',
		on_delete=models.CASCADE
	)
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code



###* Tools.Items10 *### (uid.unique)
class Items_Test10(models.Model):
	class Meta:
		db_table = 'Items_Test10'
		verbose_name = 'Items_010'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=5, unique=True )
	hinmoku = models.CharField( "種別", default=None, max_length=255 )
	h_name = models.CharField( "品目名", default=None, max_length=255 )
	sc1 = models.CharField( "ショートカット1", default=None, max_length=255 )
	sc2 = models.CharField( "ショートカット2", default=None, max_length=255 )
	name = models.CharField( "正式名称", default=None, max_length=255 )

	def __str__(self):
		return self.uid


###* Guest.Name.010 *### ( uid : unique )
class Name_Test10(models.Model):
	class Meta:
		db_table = 'Name_Test10'
		verbose_name = 'Name_010'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	# id = models.AutoField( "id", primary_key=True )
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16, unique=True )
	# uid  = models.CharField( "共通ID", default=None, unique=True, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	name_furigana = models.CharField( "顧客フリガナ", default=None, max_length=255 )

	def __str__(self):
		return self.uid

###* Guest.Name.020 *### ( uid : IntegerField, unique )
class Name_Test20(models.Model):
	class Meta:
		db_table = 'Name_Test20'
		verbose_name = 'Name_020'
		verbose_name_plural = verbose_name
		ordering = ['uid']
	# id = models.AutoField( "id", primary_key=True )
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None, unique=True )
	# uid  = models.CharField( "共通ID", default=None, unique=True, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	name_furigana = models.CharField( "顧客フリガナ", default=None, max_length=255 )

	def __str__(self):
		return self.uid

###* Guest.Bank020 *###
class Bank_Test20(models.Model):
	class Meta:
		db_table = 'Bank_Test20'
		verbose_name = 'Bank_020'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None, unique=True )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	bank_name = models.CharField( "銀行名", default=None, max_length=255 )
	bank_number = models.PositiveSmallIntegerField( "銀行番号", default=None)
	branch_number = models.PositiveSmallIntegerField( "支店番号", default=None )
	account_kind = models.CharField( "口座種類", default=None, max_length=255 )
	account = models.PositiveIntegerField( "口座番号", default=None )
	check_day = models.PositiveSmallIntegerField( "締切日", default=None )
	receipt = models.PositiveSmallIntegerField( "領収書添付有無", default=None )
	s_format = models.PositiveSmallIntegerField( "請求書フォーマット", default=None )
	r_code	= models.IntegerField( verbose_name='掛現金/掛振込', default=0 )

	def __str__(self):
		return self.uid


###* SHARP.020 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP_Test20(models.Model):
	class Meta:
		db_table = 'SHARP_Test20'
		verbose_name = 'SHARP_020'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_datetime 	= models.DateTimeField( verbose_name='取引日時' )		# 0000-00-00 00:00
	# m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	# m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test20',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='sharp20',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test10',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='sharp20',
		on_delete=models.CASCADE
	)
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code



###* SHARP.010 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP_Test10(models.Model):
	class Meta:
		db_table = 'SHARP_Test10'
		verbose_name = 'SHARP_010'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_datetime 	= models.DateTimeField( verbose_name='取引日時' )		# 0000-00-00 00:00
	# m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	# m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test10',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='sharp10',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test10',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='sharp10',
		on_delete=models.CASCADE
	)
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code



###* Invoice.020 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class Invoice_Test20(models.Model):
	class Meta:
		db_table = 'Invoice_Test20'
		verbose_name = 'Invoice_020'
		verbose_name_plural = verbose_name
		ordering = ['m_datetime']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_datetime 	= models.DateTimeField( verbose_name='取引日時' )		# 0000-00-00 00:00
	# m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	# m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test20',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='invoice20',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test10',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='invoice20',
		on_delete=models.CASCADE
	)
	# amount	= models.IntegerField( verbose_name='数量', default=0 )						# max_length=8,
	amount	= models.FloatField( verbose_name='数量', default=0 )						# max_length=8,
	unit	= models.FloatField( verbose_name='単価', default=0 )						# max_length=8,
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code



###* Invoice.010 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class Invoice_Test10(models.Model):
	class Meta:
		db_table = 'Invoice_Test10'
		verbose_name = 'Invoice_010'
		verbose_name_plural = verbose_name
		ordering = ['m_datetime']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_datetime 	= models.DateTimeField( verbose_name='取引日時' )		# 0000-00-00 00:00
	# m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	# m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test10',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='invoice10',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test10',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='invoice10',
		on_delete=models.CASCADE
	)
	# amount	= models.IntegerField( verbose_name='数量', default=0 )						# max_length=8,
	amount	= models.FloatField( verbose_name='数量', default=0 )						# max_length=8,
	unit	= models.FloatField( verbose_name='単価', default=0 )						# max_length=8,
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* Invoice.000 *### (g_code:ForeignKey, s_code:ForeignKey)
'''
class Invoice_Test(models.Model):
	class Meta:
		db_table = 'Invoice_Test'
		verbose_name = 'Invoice_000'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_day 	= models.IntegerField( verbose_name='取引日', default=0 )					# max_length=8,
	m_time	= models.IntegerField( verbose_name='時間', default=0 )						# max_length=4,
	p_code	= models.CharField( verbose_name='処理区分', default=None, max_length=2 )
	d_type	= models.CharField( verbose_name='データ種類', default=None, max_length=3 )
	r_code	= models.IntegerField( verbose_name='現金/掛コード', default=0 )				# max_length=1,
	ss_code	= models.CharField( verbose_name='SSコード', default=None, max_length=5 )
	# g_code	= models.CharField( verbose_name='顧客コード', default=None, max_length=4 )
	g_code = models.ForeignKey( 'Name_Test02',
		verbose_name='顧客コード',
		db_column='g_code',
		to_field='uid',
		related_name='invoice',
		on_delete=models.CASCADE
	)
	# g_code = models.OneToOneField('Name_Test02', verbose_name='顧客コード', db_column='g_code', to_field='uid', related_name='sharp03', on_delete=models.CASCADE)
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
	# product	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	# s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )
	s_code	= models.ForeignKey( 'Items_Test02',
		verbose_name='商品',
		db_column='s_code',
		to_field='uid',
		related_name='invoice',
		on_delete=models.CASCADE
	)
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
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code
'''

###* DayTime.000 *###
'''
class DayTime_Test(models.Model):
	class Meta:
		db_table = 'DayTime_Test'
		verbose_name = 'DayTime_000'
		verbose_name_plural = verbose_name
		ordering = ['id']
	id 		= models.IntegerField( verbose_name='id', unique=True, primary_key=True )	# max_length=4
	m_date 	= models.DateField( verbose_name='取引日' )		# max_length=8
	# m_date 	= models.DateField( verbose_name='取引日', input_formats=settings.DATETIME_FORMAT )		# max_length=8
	m_time 	= models.DateTimeField( verbose_name='取引時刻' )		# max_length=8
	# m_time 	= models.DateTimeField( verbose_name='取引時刻' )		# max_length=8
	# m_time 	= models.DateTimeField( verbose_name='取引時刻', auto_now=False )		# max_length=8

	def __str__(self):
		return self.id
'''
