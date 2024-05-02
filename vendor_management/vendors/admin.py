from django.contrib import admin
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']

# Register your models here.

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)
