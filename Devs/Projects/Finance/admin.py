#//+------------------------------------------------------------------+
#//|                     VerysVeryInc.Python3.Django.Finance.Admin.py |
#//|                  Copyright(c) 2018, VerysVery Inc. & Yoshio.Mr24 |
#//|                 https://github.com/MatsuoStation/Python3.Django/ |
#//|                                                 Since:2018.03.05 |
#//|                                Released under the Apache license |
#//|                       https://opensource.org/licenses/Apache-2.0 |
#//|  "VsV.Python3.Dj.Finance.Admin.py - Ver.3.5.3 Update:2018.03.13" |
#//+------------------------------------------------------------------+
from django.contrib import admin

# Register your models here.
### MatsuoStation.Com ###
from .models import Name_Test, Bank_Test, Add_Test, Tel_Test, Value_Test
from .models import Items_Test
from .models import SHARP_Test


class NameAdmin(admin.ModelAdmin):
	list_display = ('uid', 'name', 'name_furigana')
	search_fields = ['uid','name', 'name_furigana']

class BankAdmin(admin.ModelAdmin):
	list_display = ('uid', 'bank_name', 'bank_number', 'branch_number', 'account_kind', 'account', 'check_day', 'receipt', 's_format')
	search_fields = [ 'uid', 'check_day', 'bank_name', 'bank_number' ]

class AddAdmin(admin.ModelAdmin):
	list_display = ('uid', 'postal_code', 'address')
	search_fields = [ 'uid', 'postal_code', 'address' ]

class TelAdmin(admin.ModelAdmin):
	list_display = ('uid', 'phone', 'mobile_tel')
	search_fields = [ 'uid', 'phone', 'mobile_tel' ]

class ValueAdmin(admin.ModelAdmin):
	list_display = ('uid', 's_code', 'day', 'value', 'date01', 'value01', 'date02', 'value02', 'date03', 'value03')
	search_fields = [ 'uid', 's_code', 'day' ]

class iTemsAdmin(admin.ModelAdmin):
	list_display = ('id', 'uid', 'hinmoku', 'h_name')
	search_fields = [ 'uid', ]

class SHARPAdmin(admin.ModelAdmin):
	list_display = ('id', 'day', 'time', 'p_code', 'd_type', 'r_code', 'g_code', 'car_code', 'red_code', 'slip', 's_code', 'amount', 'unit', 'value')
	search_fields = [ 'g_code', ]

admin.site.register(Name_Test, NameAdmin)
admin.site.register(Bank_Test, BankAdmin)
admin.site.register(Add_Test, AddAdmin)
admin.site.register(Tel_Test, TelAdmin)
admin.site.register(Value_Test, ValueAdmin)

admin.site.register(Items_Test, iTemsAdmin)
admin.site.register(SHARP_Test, SHARPAdmin)
