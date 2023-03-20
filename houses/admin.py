from django.contrib import admin
from .models import House


class HouseAdmin(admin.ModelAdmin):
    list_display = ('house_name', 'rent', 'utilities', 'water_meter_reading', 'rent_status')
    list_filter = ('rent_status',)
    search_fields = ('house_name',)

admin.site.register(House, HouseAdmin)