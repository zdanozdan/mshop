from mshop.models import MikranProduct
from django.contrib import admin

class MikranProductAdmin(admin.ModelAdmin):
    list_display = ('id','get_name','slug','vat', 'native_price')
    search_fields = ['id','name']

    #list_filter = ('model__name','name','type')

admin.site.register(MikranProduct, MikranProductAdmin)
