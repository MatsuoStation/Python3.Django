#//+------------------------------------------------------------------+
#//|                    VerysVeryInc.Python3.Django.Finance.Models.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|   "VsV.Py3.Dj.Finance.Models.py - Ver.3.20.30 Update:2019.09.15" |
#//+------------------------------------------------------------------+
from django.db import models

# Create your models here.
### MatsuoStation.Com ###
from django.conf import settings


# settings.DATETIME_FORMAT

###* SHARP20.K_2020 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP20_K_2020(models.Model):
	class Meta:
		db_table = 'SHARP20_K_2020'
		verbose_name = 'SHARP20_K_2020'
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
		related_name='sharp20_k_2020',
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
		related_name='sharp20_k_2020',
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
	# c_day 	= models.DateTimeField( verbose_name='伝票年月日(修正)' )						# 0000-00-00 00:00
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* SHARP20.K_2019 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP20_K_2019(models.Model):
	class Meta:
		db_table = 'SHARP20_K_2019'
		verbose_name = 'SHARP20_K_2019'
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
		related_name='sharp20_k_2019',
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
		related_name='sharp20_k_2019',
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
	# c_day 	= models.DateTimeField( verbose_name='伝票年月日(修正)' )						# 0000-00-00 00:00
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* SHARP20.K_2018 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP20_K_2018(models.Model):
	class Meta:
		db_table = 'SHARP20_K_2018'
		verbose_name = 'SHARP20_K_2018'
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
		related_name='sharp20_k_2018',
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
		related_name='sharp20_k_2018',
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
	# c_day 	= models.DateTimeField( verbose_name='伝票年月日(修正)' )						# 0000-00-00 00:00
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* SHARP20.K_2017 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP20_K_2017(models.Model):
	class Meta:
		db_table = 'SHARP20_K_2017'
		verbose_name = 'SHARP20_K_2017'
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
		related_name='sharp20_k_2017',
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
		related_name='sharp20_k_2017',
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
	# c_day 	= models.DateTimeField( verbose_name='伝票年月日(修正)' )						# 0000-00-00 00:00
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* SHARP20.K_2016 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP20_K_2016(models.Model):
	class Meta:
		db_table = 'SHARP20_K_2016'
		verbose_name = 'SHARP20_K_2016'
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
		related_name='sharp20_k_2016',
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
		related_name='sharp20_k_2016',
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
	# c_day 	= models.DateTimeField( verbose_name='伝票年月日(修正)' )						# 0000-00-00 00:00
	c_day	= models.IntegerField( verbose_name='伝票年月日(修正)', default=0 )			# max_length=8,
	c_no	= models.CharField( verbose_name='伝票No(修正)', default=None, max_length=4 )
	sub_data= models.CharField( verbose_name='サブデータ(修正)', default=None, max_length=8 )
	ss_dev	= models.CharField( verbose_name='SSコード(修正)', default=None, max_length=10 )
	# name_id = models.ForeignKey('Name_Test', on_delete=models.CASCADE)

	def __str__(self):
		return self.s_code


###* InCash.020 *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class InCash_Test20(models.Model):
	class Meta:
		db_table = 'InCash_Test20'
		verbose_name = 'InCash_020'
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

	g_code	= models.IntegerField( verbose_name='顧客コード', default=None )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )

	def __str__(self):
		return self.s_code


###* LPG.Meter00 *### (uid : IntegerField)
class LPG_Meter00(models.Model):
	class Meta:
		db_table = 'LPG_Meter00'
		verbose_name = 'LPT_Meter_000'
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


###* LPG.Meter10 *### (uid : IntegerField)
class LPG_Meter10(models.Model):
	class Meta:
		db_table = 'LPG_Meter10'
		verbose_name = 'LPT_Meter_010'
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
	indate0		= models.DateTimeField( verbose_name='入金日0' )
	invalue0	= models.IntegerField( verbose_name='入金金額0', default=0 )
	indate00	= models.DateTimeField( verbose_name='入金日00' )
	invalue00	= models.IntegerField( verbose_name='入金金額00', default=0 )

	date01 	= models.DateTimeField( verbose_name='検針日01' )
	meter01	= models.FloatField( "検針値01", default=None )
	amount01= models.FloatField( "使用量01", default=None )
	indate1		= models.DateTimeField( verbose_name='入金日1' )
	invalue1	= models.IntegerField( verbose_name='入金金額1', default=0 )
	indate01	= models.DateTimeField( verbose_name='入金日01' )
	invalue01	= models.IntegerField( verbose_name='入金金額01', default=0 )

	date02 	= models.DateTimeField( verbose_name='検針日02' )
	meter02	= models.FloatField( "検針値02", default=None )
	amount02= models.FloatField( "使用量02", default=None )
	indate2		= models.DateTimeField( verbose_name='入金日2' )
	invalue2	= models.IntegerField( verbose_name='入金金額2', default=0 )
	indate02	= models.DateTimeField( verbose_name='入金日02' )
	invalue02	= models.IntegerField( verbose_name='入金金額02', default=0 )

	date03 	= models.DateTimeField( verbose_name='検針日03' )
	meter03	= models.FloatField( "検針値03", default=None )
	amount03= models.FloatField( "使用量03", default=None )
	indate3		= models.DateTimeField( verbose_name='入金日3' )
	invalue3	= models.IntegerField( verbose_name='入金金額3', default=0 )
	indate03	= models.DateTimeField( verbose_name='入金日03' )
	invalue03	= models.IntegerField( verbose_name='入金金額03', default=0 )

	date04 	= models.DateTimeField( verbose_name='検針日04' )
	meter04	= models.FloatField( "検針値04", default=None )
	amount04= models.FloatField( "使用量04", default=None )
	indate4		= models.DateTimeField( verbose_name='入金日4' )
	invalue4	= models.IntegerField( verbose_name='入金金額4', default=0 )
	indate04	= models.DateTimeField( verbose_name='入金日04' )
	invalue04	= models.IntegerField( verbose_name='入金金額04', default=0 )

	date05 	= models.DateTimeField( verbose_name='検針日05' )
	meter05	= models.FloatField( "検針値05", default=None )
	amount05= models.FloatField( "使用量05", default=None )
	indate5		= models.DateTimeField( verbose_name='入金日5' )
	invalue5	= models.IntegerField( verbose_name='入金金額5', default=0 )
	indate05	= models.DateTimeField( verbose_name='入金日05' )
	invalue05	= models.IntegerField( verbose_name='入金金額05', default=0 )

	date06 	= models.DateTimeField( verbose_name='検針日06' )
	meter06	= models.FloatField( "検針値06", default=None )
	amount06= models.FloatField( "使用量06", default=None )
	indate6		= models.DateTimeField( verbose_name='入金日6' )
	invalue6	= models.IntegerField( verbose_name='入金金額6', default=0 )
	indate06	= models.DateTimeField( verbose_name='入金日06' )
	invalue06	= models.IntegerField( verbose_name='入金金額06', default=0 )

	date07 	= models.DateTimeField( verbose_name='検針日07' )
	meter07	= models.FloatField( "検針値07", default=None )
	amount07= models.FloatField( "使用量07", default=None )
	indate7		= models.DateTimeField( verbose_name='入金日7' )
	invalue7	= models.IntegerField( verbose_name='入金金額7', default=0 )
	indate07	= models.DateTimeField( verbose_name='入金日07' )
	invalue07	= models.IntegerField( verbose_name='入金金額07', default=0 )

	date08 	= models.DateTimeField( verbose_name='検針日08' )
	meter08	= models.FloatField( "検針値08", default=None )
	amount08= models.FloatField( "使用量08", default=None )
	indate8		= models.DateTimeField( verbose_name='入金日8' )
	invalue8	= models.IntegerField( verbose_name='入金金額8', default=0 )
	indate08	= models.DateTimeField( verbose_name='入金日08' )
	invalue08	= models.IntegerField( verbose_name='入金金額08', default=0 )

	date09 	= models.DateTimeField( verbose_name='検針日09' )
	meter09	= models.FloatField( "検針値09", default=None )
	amount09= models.FloatField( "使用量09", default=None )
	indate9		= models.DateTimeField( verbose_name='入金日9' )
	invalue9	= models.IntegerField( verbose_name='入金金額9', default=0 )
	indate09	= models.DateTimeField( verbose_name='入金日09' )
	invalue09	= models.IntegerField( verbose_name='入金金額09', default=0 )

	date10 	= models.DateTimeField( verbose_name='検針日10' )
	meter10	= models.FloatField( "検針値10", default=None )
	amount10= models.FloatField( "使用量10", default=None )
	indate10	= models.DateTimeField( verbose_name='入金日10' )
	invalue10	= models.IntegerField( verbose_name='入金金額10', default=0 )
	indate010	= models.DateTimeField( verbose_name='入金日010' )
	invalue010	= models.IntegerField( verbose_name='入金金額010', default=0 )

	date11 	= models.DateTimeField( verbose_name='検針日11' )
	meter11	= models.FloatField( "検針値11", default=None )
	amount11= models.FloatField( "使用量11", default=None )
	indate11	= models.DateTimeField( verbose_name='入金日11' )
	invalue11	= models.IntegerField( verbose_name='入金金額11', default=0 )
	indate011	= models.DateTimeField( verbose_name='入金日011' )
	invalue011	= models.IntegerField( verbose_name='入金金額011', default=0 )

	date12 	= models.DateTimeField( verbose_name='検針日12' )
	meter12	= models.FloatField( "検針値12", default=None )
	amount12= models.FloatField( "使用量12", default=None )
	indate12	= models.DateTimeField( verbose_name='入金日12' )
	invalue12	= models.IntegerField( verbose_name='入金金額12', default=0 )
	indate012	= models.DateTimeField( verbose_name='入金日012' )
	invalue012	= models.IntegerField( verbose_name='入金金額012', default=0 )

	date13 	= models.DateTimeField( verbose_name='検針日13', blank=True, null=True  )
	meter13	= models.FloatField( "検針値13", default=None )
	amount13= models.FloatField( "使用量13", default=None )
	indate13	= models.DateTimeField( verbose_name='入金日13', blank=True, null=True  )
	invalue13	= models.IntegerField( verbose_name='入金金額13', default=0 )
	indate013	= models.DateTimeField( verbose_name='入金日013', blank=True, null=True  )
	invalue013	= models.IntegerField( verbose_name='入金金額013', default=0 )

	date14 	= models.DateTimeField( verbose_name='検針日14', blank=True, null=True  )
	meter14	= models.FloatField( "検針値14", default=None )
	amount14= models.FloatField( "使用量14", default=None )
	indate14	= models.DateTimeField( verbose_name='入金日14', blank=True, null=True  )
	invalue14	= models.IntegerField( verbose_name='入金金額14', default=0 )
	indate014	= models.DateTimeField( verbose_name='入金日014', blank=True, null=True  )
	invalue014	= models.IntegerField( verbose_name='入金金額014', default=0 )

	date15 	= models.DateTimeField( verbose_name='検針日15', blank=True, null=True  )
	meter15	= models.FloatField( "検針値15", default=None )
	amount15= models.FloatField( "使用量15", default=None )
	indate15	= models.DateTimeField( verbose_name='入金日15', blank=True, null=True  )
	invalue15	= models.IntegerField( verbose_name='入金金額15', default=0 )
	indate015	= models.DateTimeField( verbose_name='入金日015', blank=True, null=True  )
	invalue015	= models.IntegerField( verbose_name='入金金額015', default=0 )

	date16 	= models.DateTimeField( verbose_name='検針日16', blank=True, null=True  )
	meter16	= models.FloatField( "検針値16", default=None )
	amount16= models.FloatField( "使用量16", default=None )
	indate16	= models.DateTimeField( verbose_name='入金日16', blank=True, null=True  )
	invalue16	= models.IntegerField( verbose_name='入金金額16', default=0 )
	indate016	= models.DateTimeField( verbose_name='入金日016', blank=True, null=True  )
	invalue016	= models.IntegerField( verbose_name='入金金額016', default=0 )

	date17 	= models.DateTimeField( verbose_name='検針日17', blank=True, null=True  )
	meter17	= models.FloatField( "検針値17", default=None )
	amount17= models.FloatField( "使用量17", default=None )
	indate17	= models.DateTimeField( verbose_name='入金日17', blank=True, null=True  )
	invalue17	= models.IntegerField( verbose_name='入金金額17', default=0 )
	indate017	= models.DateTimeField( verbose_name='入金日017', blank=True, null=True  )
	invalue017	= models.IntegerField( verbose_name='入金金額017', default=0 )

	date18 	= models.DateTimeField( verbose_name='検針日18', blank=True, null=True  )
	meter18	= models.FloatField( "検針値18", default=None )
	amount18= models.FloatField( "使用量18", default=None )
	indate18	= models.DateTimeField( verbose_name='入金日18', blank=True, null=True  )
	invalue18	= models.IntegerField( verbose_name='入金金額18', default=0 )
	indate018	= models.DateTimeField( verbose_name='入金日018', blank=True, null=True  )
	invalue018	= models.IntegerField( verbose_name='入金金額018', default=0 )

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


###* LPG.Toyu.Jyuyu.00 *### (uid : IntegerField)
class LPG_ToJyu00(models.Model):
	class Meta:
		db_table = 'LPG_ToJyu00'
		verbose_name = 'LPT_ToJyu_000'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.IntegerField( "共通ID", default=None )
	name = models.CharField( "顧客名", default=None, max_length=255 )

	s_code00= models.CharField( verbose_name='商品00', default=None, max_length=5 )
	date00 	= models.DateTimeField( verbose_name='取引日00' )
	amount00= models.FloatField( "数量00", default=None )
	unit00	= models.FloatField( "単価00", default=None )
	value00	= models.IntegerField( verbose_name='税別金額00', default=0 )
	indate0		= models.DateTimeField( verbose_name='入金日0' )
	invalue0	= models.IntegerField( verbose_name='入金金額0', default=0 )
	indate00	= models.DateTimeField( verbose_name='入金日00' )
	invalue00	= models.IntegerField( verbose_name='入金金額00', default=0 )

	s_code01= models.CharField( verbose_name='商品01', default=None, max_length=5 )
	date01 	= models.DateTimeField( verbose_name='取引日01' )
	amount01= models.FloatField( "数量01", default=None )
	unit01	= models.FloatField( "単価01", default=None )
	value01	= models.IntegerField( verbose_name='税別金額01', default=0 )
	indate1		= models.DateTimeField( verbose_name='入金日1' )
	invalue1	= models.IntegerField( verbose_name='入金金額1', default=0 )
	indate01	= models.DateTimeField( verbose_name='入金日01' )
	invalue01	= models.IntegerField( verbose_name='入金金額01', default=0 )

	s_code02= models.CharField( verbose_name='商品02', default=None, max_length=5 )
	date02 	= models.DateTimeField( verbose_name='取引日02' )
	amount02= models.FloatField( "数量02", default=None )
	unit02	= models.FloatField( "単価02", default=None )
	value02	= models.IntegerField( verbose_name='税別金額02', default=0 )
	indate2		= models.DateTimeField( verbose_name='入金日2' )
	invalue2	= models.IntegerField( verbose_name='入金金額2', default=0 )
	indate02	= models.DateTimeField( verbose_name='入金日02' )
	invalue02	= models.IntegerField( verbose_name='入金金額02', default=0 )

	s_code03= models.CharField( verbose_name='商品03', default=None, max_length=5 )
	date03 	= models.DateTimeField( verbose_name='取引日03' )
	amount03= models.FloatField( "数量03", default=None )
	unit03	= models.FloatField( "単価03", default=None )
	value03	= models.IntegerField( verbose_name='税別金額03', default=0 )
	indate3		= models.DateTimeField( verbose_name='入金日3' )
	invalue3	= models.IntegerField( verbose_name='入金金額3', default=0 )
	indate03	= models.DateTimeField( verbose_name='入金日03' )
	invalue03	= models.IntegerField( verbose_name='入金金額03', default=0 )

	s_code04= models.CharField( verbose_name='商品04', default=None, max_length=5 )
	date04 	= models.DateTimeField( verbose_name='取引日04' )
	amount04= models.FloatField( "数量04", default=None )
	unit04	= models.FloatField( "単価04", default=None )
	value04	= models.IntegerField( verbose_name='税別金額04', default=0 )
	indate4		= models.DateTimeField( verbose_name='入金日4' )
	invalue4	= models.IntegerField( verbose_name='入金金額4', default=0 )
	indate04	= models.DateTimeField( verbose_name='入金日04' )
	invalue04	= models.IntegerField( verbose_name='入金金額04', default=0 )

	s_code05= models.CharField( verbose_name='商品05', default=None, max_length=5 )
	date05 	= models.DateTimeField( verbose_name='取引日05' )
	amount05= models.FloatField( "数量05", default=None )
	unit05	= models.FloatField( "単価05", default=None )
	value05	= models.IntegerField( verbose_name='税別金額05', default=0 )
	indate5		= models.DateTimeField( verbose_name='入金日5' )
	invalue5	= models.IntegerField( verbose_name='入金金額5', default=0 )
	indate05	= models.DateTimeField( verbose_name='入金日05' )
	invalue05	= models.IntegerField( verbose_name='入金金額05', default=0 )

	s_code06= models.CharField( verbose_name='商品06', default=None, max_length=5 )
	date06 	= models.DateTimeField( verbose_name='取引日06' )
	amount06= models.FloatField( "数量06", default=None )
	unit06	= models.FloatField( "単価06", default=None )
	value06	= models.IntegerField( verbose_name='税別金額06', default=0 )
	indate6		= models.DateTimeField( verbose_name='入金日6' )
	invalue6	= models.IntegerField( verbose_name='入金金額6', default=0 )
	indate06	= models.DateTimeField( verbose_name='入金日06' )
	invalue06	= models.IntegerField( verbose_name='入金金額06', default=0 )

	s_code07= models.CharField( verbose_name='商品07', default=None, max_length=5 )
	date07 	= models.DateTimeField( verbose_name='取引日07' )
	amount07= models.FloatField( "数量07", default=None )
	unit07	= models.FloatField( "単価07", default=None )
	value07	= models.IntegerField( verbose_name='税別金額07', default=0 )
	indate7		= models.DateTimeField( verbose_name='入金日7' )
	invalue7	= models.IntegerField( verbose_name='入金金額7', default=0 )
	indate07	= models.DateTimeField( verbose_name='入金日07' )
	invalue07	= models.IntegerField( verbose_name='入金金額07', default=0 )

	s_code08= models.CharField( verbose_name='商品08', default=None, max_length=5 )
	date08 	= models.DateTimeField( verbose_name='取引日08' )
	amount08= models.FloatField( "数量08", default=None )
	unit08	= models.FloatField( "単価08", default=None )
	value08	= models.IntegerField( verbose_name='税別金額08', default=0 )
	indate8		= models.DateTimeField( verbose_name='入金日8' )
	invalue8	= models.IntegerField( verbose_name='入金金額8', default=0 )
	indate08	= models.DateTimeField( verbose_name='入金日08' )
	invalue08	= models.IntegerField( verbose_name='入金金額08', default=0 )

	s_code09= models.CharField( verbose_name='商品09', default=None, max_length=5 )
	date09 	= models.DateTimeField( verbose_name='取引日09' )
	amount09= models.FloatField( "数量09", default=None )
	unit09	= models.FloatField( "単価09", default=None )
	value09	= models.IntegerField( verbose_name='税別金額09', default=0 )
	indate9		= models.DateTimeField( verbose_name='入金日9' )
	invalue9	= models.IntegerField( verbose_name='入金金額9', default=0 )
	indate09	= models.DateTimeField( verbose_name='入金日09' )
	invalue09	= models.IntegerField( verbose_name='入金金額09', default=0 )

	s_code10= models.CharField( verbose_name='商品10', default=None, max_length=5 )
	date10 	= models.DateTimeField( verbose_name='取引日10' )
	amount10= models.FloatField( "数量10", default=None )
	unit10	= models.FloatField( "単価10", default=None )
	value10	= models.IntegerField( verbose_name='税別金額10', default=0 )
	indate10	= models.DateTimeField( verbose_name='入金日10' )
	invalue10	= models.IntegerField( verbose_name='入金金額10', default=0 )
	indate010	= models.DateTimeField( verbose_name='入金日010' )
	invalue010	= models.IntegerField( verbose_name='入金金額010', default=0 )

	s_code11= models.CharField( verbose_name='商品11', default=None, max_length=5 )
	date11 	= models.DateTimeField( verbose_name='取引日11' )
	amount11= models.FloatField( "数量11", default=None )
	unit11	= models.FloatField( "単価11", default=None )
	value11	= models.IntegerField( verbose_name='税別金額11', default=0 )
	indate11	= models.DateTimeField( verbose_name='入金日11' )
	invalue11	= models.IntegerField( verbose_name='入金金額11', default=0 )
	indate011	= models.DateTimeField( verbose_name='入金日011' )
	invalue011	= models.IntegerField( verbose_name='入金金額011', default=0 )

	s_code12= models.CharField( verbose_name='商品12', default=None, max_length=5 )
	date12 	= models.DateTimeField( verbose_name='取引日12' )
	amount12= models.FloatField( "数量12", default=None )
	unit12	= models.FloatField( "単価12", default=None )
	value12	= models.IntegerField( verbose_name='税別金額12', default=0 )
	indate12	= models.DateTimeField( verbose_name='入金日12' )
	invalue12	= models.IntegerField( verbose_name='入金金額12', default=0 )
	indate012	= models.DateTimeField( verbose_name='入金日012' )
	invalue012	= models.IntegerField( verbose_name='入金金額012', default=0 )

	s_code13= models.CharField( verbose_name='商品13', default=None, max_length=5 )
	date13 	= models.DateTimeField( verbose_name='取引日13' )
	amount13= models.FloatField( "数量13", default=None )
	unit13	= models.FloatField( "単価13", default=None )
	value13	= models.IntegerField( verbose_name='税別金額13', default=0 )
	indate13	= models.DateTimeField( verbose_name='入金日13' )
	invalue13	= models.IntegerField( verbose_name='入金金額13', default=0 )
	indate013	= models.DateTimeField( verbose_name='入金日013' )
	invalue013	= models.IntegerField( verbose_name='入金金額013', default=0 )

	s_code14= models.CharField( verbose_name='商品14', default=None, max_length=5 )
	date14 	= models.DateTimeField( verbose_name='取引日14' )
	amount14= models.FloatField( "数量14", default=None )
	unit14	= models.FloatField( "単価14", default=None )
	value14	= models.IntegerField( verbose_name='税別金額14', default=0 )
	indate14	= models.DateTimeField( verbose_name='入金日14' )
	invalue14	= models.IntegerField( verbose_name='入金金額14', default=0 )
	indate014	= models.DateTimeField( verbose_name='入金日014' )
	invalue014	= models.IntegerField( verbose_name='入金金額014', default=0 )

	s_code15= models.CharField( verbose_name='商品15', default=None, max_length=5 )
	date15 	= models.DateTimeField( verbose_name='取引日15' )
	amount15= models.FloatField( "数量15", default=None )
	unit15	= models.FloatField( "単価15", default=None )
	value15	= models.IntegerField( verbose_name='税別金額15', default=0 )
	indate15	= models.DateTimeField( verbose_name='入金日15' )
	invalue15	= models.IntegerField( verbose_name='入金金額15', default=0 )
	indate015	= models.DateTimeField( verbose_name='入金日015' )
	invalue015	= models.IntegerField( verbose_name='入金金額015', default=0 )

	s_code16= models.CharField( verbose_name='商品16', default=None, max_length=5 )
	date16 	= models.DateTimeField( verbose_name='取引日16' )
	amount16= models.FloatField( "数量16", default=None )
	unit16	= models.FloatField( "単価16", default=None )
	value16	= models.IntegerField( verbose_name='税別金額16', default=0 )
	indate16	= models.DateTimeField( verbose_name='入金日16' )
	invalue16	= models.IntegerField( verbose_name='入金金額16', default=0 )
	indate016	= models.DateTimeField( verbose_name='入金日016' )
	invalue016	= models.IntegerField( verbose_name='入金金額016', default=0 )

	s_code17= models.CharField( verbose_name='商品17', default=None, max_length=5 )
	date17 	= models.DateTimeField( verbose_name='取引日17' )
	amount17= models.FloatField( "数量17", default=None )
	unit17	= models.FloatField( "単価17", default=None )
	value17	= models.IntegerField( verbose_name='税別金額17', default=0 )
	indate17	= models.DateTimeField( verbose_name='入金日17' )
	invalue17	= models.IntegerField( verbose_name='入金金額17', default=0 )
	indate017	= models.DateTimeField( verbose_name='入金日017' )
	invalue017	= models.IntegerField( verbose_name='入金金額017', default=0 )

	s_code18= models.CharField( verbose_name='商品18', default=None, max_length=5 )
	date18 	= models.DateTimeField( verbose_name='取引日18' )
	amount18= models.FloatField( "数量18", default=None )
	unit18	= models.FloatField( "単価18", default=None )
	value18	= models.IntegerField( verbose_name='税別金額18', default=0 )
	indate18	= models.DateTimeField( verbose_name='入金日18' )
	invalue18	= models.IntegerField( verbose_name='入金金額18', default=0 )
	indate018	= models.DateTimeField( verbose_name='入金日018' )
	invalue018	= models.IntegerField( verbose_name='入金金額018', default=0 )

	s_code19= models.CharField( verbose_name='商品19', default=None, max_length=5 )
	date19 	= models.DateTimeField( verbose_name='取引日19' )
	amount19= models.FloatField( "数量19", default=None )
	unit19	= models.FloatField( "単価19", default=None )
	value19	= models.IntegerField( verbose_name='税別金額19', default=0 )
	indate19	= models.DateTimeField( verbose_name='入金日19' )
	invalue19	= models.IntegerField( verbose_name='入金金額19', default=0 )
	indate019	= models.DateTimeField( verbose_name='入金日019' )
	invalue019	= models.IntegerField( verbose_name='入金金額019', default=0 )

	s_code20= models.CharField( verbose_name='商品20', default=None, max_length=5 )
	date20 	= models.DateTimeField( verbose_name='取引日20' )
	amount20= models.FloatField( "数量20", default=None )
	unit20	= models.FloatField( "単価20", default=None )
	value20	= models.IntegerField( verbose_name='税別金額20', default=0 )
	indate20	= models.DateTimeField( verbose_name='入金日20' )
	invalue20	= models.IntegerField( verbose_name='入金金額20', default=0 )
	indate020	= models.DateTimeField( verbose_name='入金日020' )
	invalue020	= models.IntegerField( verbose_name='入金金額020', default=0 )

	s_code21= models.CharField( verbose_name='商品21', default=None, max_length=5 )
	date21 	= models.DateTimeField( verbose_name='取引日21' )
	amount21= models.FloatField( "数量21", default=None )
	unit21	= models.FloatField( "単価21", default=None )
	value21	= models.IntegerField( verbose_name='税別金額21', default=0 )
	indate21	= models.DateTimeField( verbose_name='入金日21' )
	invalue21	= models.IntegerField( verbose_name='入金金額21', default=0 )
	indate021	= models.DateTimeField( verbose_name='入金日021' )
	invalue021	= models.IntegerField( verbose_name='入金金額021', default=0 )

	s_code22= models.CharField( verbose_name='商品22', default=None, max_length=5 )
	date22 	= models.DateTimeField( verbose_name='取引日22' )
	amount22= models.FloatField( "数量22", default=None )
	unit22	= models.FloatField( "単価22", default=None )
	value22	= models.IntegerField( verbose_name='税別金額22', default=0 )
	indate22	= models.DateTimeField( verbose_name='入金日22' )
	invalue22	= models.IntegerField( verbose_name='入金金額22', default=0 )
	indate022	= models.DateTimeField( verbose_name='入金日022' )
	invalue022	= models.IntegerField( verbose_name='入金金額022', default=0 )

	s_code23= models.CharField( verbose_name='商品23', default=None, max_length=5 )
	date23 	= models.DateTimeField( verbose_name='取引日23' )
	amount23= models.FloatField( "数量23", default=None )
	unit23	= models.FloatField( "単価23", default=None )
	value23	= models.IntegerField( verbose_name='税別金額23', default=0 )
	indate23	= models.DateTimeField( verbose_name='入金日23' )
	invalue23	= models.IntegerField( verbose_name='入金金額23', default=0 )
	indate023	= models.DateTimeField( verbose_name='入金日023' )
	invalue023	= models.IntegerField( verbose_name='入金金額023', default=0 )

	s_code24= models.CharField( verbose_name='商品24', default=None, max_length=5 )
	date24 	= models.DateTimeField( verbose_name='取引日24' )
	amount24= models.FloatField( "数量24", default=None )
	unit24	= models.FloatField( "単価24", default=None )
	value24	= models.IntegerField( verbose_name='税別金額24', default=0 )
	indate24	= models.DateTimeField( verbose_name='入金日24' )
	invalue24	= models.IntegerField( verbose_name='入金金額24', default=0 )
	indate024	= models.DateTimeField( verbose_name='入金日024' )
	invalue024	= models.IntegerField( verbose_name='入金金額024', default=0 )

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

	date01	= models.DateTimeField( "設定日01", blank=True, null=True)
	value01	= models.FloatField( "価格01", default=None )
	date02	= models.DateTimeField( "設定日02", blank=True, null=True)
	value02	= models.FloatField( "価格02", default=None )
	date03	= models.DateTimeField( "設定日03", blank=True, null=True)
	value03	= models.FloatField( "価格03", default=None )
	date04	= models.DateTimeField( "設定日04", blank=True, null=True)
	value04	= models.FloatField( "価格04", default=None )
	date05	= models.DateTimeField( "設定日05", blank=True, null=True)
	value05	= models.FloatField( "価格05", default=None )

	date06	= models.DateTimeField( "設定日06", blank=True, null=True)
	value06	= models.FloatField( "価格06", default=None )
	date07	= models.DateTimeField( "設定日07", blank=True, null=True)
	value07	= models.FloatField( "価格07", default=None )
	date08	= models.DateTimeField( "設定日08", blank=True, null=True)
	value08	= models.FloatField( "価格08", default=None )
	date09	= models.DateTimeField( "設定日09", blank=True, null=True)
	value09	= models.FloatField( "価格09", default=None )
	date10	= models.DateTimeField( "設定日10", blank=True, null=True)
	value10	= models.FloatField( "価格10", default=None )

	date11	= models.DateTimeField( "設定日11", blank=True, null=True)
	value11	= models.FloatField( "価格11", default=None )
	date12	= models.DateTimeField( "設定日12", blank=True, null=True)
	value12	= models.FloatField( "価格12", default=None )
	date13	= models.DateTimeField( "設定日13", blank=True, null=True)
	value13	= models.FloatField( "価格13", default=None )
	date14	= models.DateTimeField( "設定日14", blank=True, null=True)
	value14	= models.FloatField( "価格14", default=None )
	date15	= models.DateTimeField( "設定日15", blank=True, null=True)
	value15	= models.FloatField( "価格15", default=None )

	date16	= models.DateTimeField( "設定日16", blank=True, null=True)
	value16	= models.FloatField( "価格16", default=None )
	date17	= models.DateTimeField( "設定日17", blank=True, null=True)
	value17	= models.FloatField( "価格17", default=None )
	date18	= models.DateTimeField( "設定日18", blank=True, null=True)
	value18	= models.FloatField( "価格18", default=None )
	date19	= models.DateTimeField( "設定日19", blank=True, null=True)
	value19	= models.FloatField( "価格19", default=None )
	date20	= models.DateTimeField( "設定日20", blank=True, null=True)
	value20	= models.FloatField( "価格20", default=None )

	date21	= models.DateTimeField( "設定日21", blank=True, null=True)
	value21	= models.FloatField( "価格21", default=None )
	date22	= models.DateTimeField( "設定日22", blank=True, null=True)
	value22	= models.FloatField( "価格22", default=None )
	date23	= models.DateTimeField( "設定日23", blank=True, null=True)
	value23	= models.FloatField( "価格23", default=None )
	date24	= models.DateTimeField( "設定日24", blank=True, null=True)
	value24	= models.FloatField( "価格24", default=None )
	date25	= models.DateTimeField( "設定日25", blank=True, null=True)
	value25	= models.FloatField( "価格25", default=None )

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

###* Guest.Address *###
class Add_Test20(models.Model):
	class Meta:
		db_table = 'Address_Test20'
		verbose_name = 'Address_020'
		verbose_name_plural = verbose_name
		ordering = ['-uid']
	id = models.AutoField( "id", primary_key=True )
	uid  = models.CharField( "共通ID", default=None, max_length=16 )
	name = models.CharField( "顧客名", default=None, max_length=255 )
	name_furigana = models.CharField( "顧客フリガナ", default=None, max_length=255 )
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
	j_code = models.PositiveSmallIntegerField( "自振有効", default=None )

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


###* SHARP.201707.Free *### ( m_datetime : DateTimeField, g_code : ForeignKeyField, s_code : ForeignKeyField )
class SHARP_Test2017(models.Model):
	class Meta:
		db_table = 'SHARP_Test2017'
		verbose_name = 'SHARP_2017'
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

	g_code	= models.IntegerField( verbose_name='顧客コード', default=None )
	s_code	= models.CharField( verbose_name='商品', default=None, max_length=5 )

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
