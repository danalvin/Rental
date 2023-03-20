from django.contrib import admin
from .models import Tenant


class TenantAdmin(admin.ModelAdmin):
    list_display = ('First_name', 'Phone_number', 'ID_number')
    search_fields = ('full_name', 'phone_number', 'ID_number')

admin.site.register(Tenant, TenantAdmin)