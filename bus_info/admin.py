from django.contrib import admin
from .models import CarType,BusInfo,CarChangeLog

#Register your models here.
class CarChangeLogInline(admin.TabularInline):
    model = CarChangeLog
    extra = 1
class BusInfoAdmin(admin.ModelAdmin):
    fieldsets=[
        ('车牌号',{'fields':['car_id']}),
        ('登记日期',{'fields':['published_date'],'classes':['collapse']}),
        ('线路',{'fields':['route']}),
        ('公司',{'fields':['company']}),
        ('车型',{'fields':['cartype']}),
        ('所属车队',{'fields':['team']})
    ]
    inlines = [CarChangeLogInline]
    list_display = ('car_id', 'route','team')
    search_fields = ['route']

class CarTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('车型', {'fields': ['type_name']}),
        ('公司简称', {'fields': ['subname']}),
        ('公司全称', {'fields': ['company_name']}),
        ('车长', {'fields': ['car_length']}),
        ('能耗类型', {'fields': ['power_type']}),
        ('载客量', {'fields': ['bus_load']}),
    ]

    list_display = ( 'type_name','subname')

admin.site.register(BusInfo,BusInfoAdmin)
admin.site.register(CarType,CarTypeAdmin)