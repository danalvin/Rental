from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from datetime import timezone

from houses.forms import MeterReadingForm, RentForm

from .models import House, Rent, Payment, MeterReading


class RentInline(admin.TabularInline):
    model = Rent
    extra = 1


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1


class HouseAdmin(admin.ModelAdmin):
    inlines = [RentInline, PaymentInline]
    list_display = ('house_name', 'address', 'rent_amount', 'meter_reading', 'get_rent_status')
    list_filter = ('rent__date',)
    search_fields = ('house_name', 'address')

    def get_rent_status(self, obj):
        latest_rent = obj.rent_set.last()
        if latest_rent:
            if latest_rent.date < timezone.now().date():
                return format_html('<span style="color:red">Overdue</span>')
            elif latest_rent.date == timezone.now().date():
                return format_html('<span style="color:orange">Due Today</span>')
            else:
                return format_html('<span style="color:green">Paid</span>')
        else:
            return '-'

    get_rent_status.short_description = 'Rent Status'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/meter-reading/',
                self.admin_site.admin_view(self.meter_reading_view),
                name='house-meter-reading',
            ),
            path(
                '<int:pk>/update-rent/',
                self.admin_site.admin_view(self.update_rent_view),
                name='house-update-rent',
            ),
        ]
        return custom_urls + urls

    def meter_reading_view(self, request, pk):
        house = self.get_object(request, pk)
        if request.method == 'POST':
            form = MeterReadingForm(request.POST)
            if form.is_valid():
                meter_reading = form.cleaned_data['meter_reading']
                house.meter_reading = meter_reading
                house.save()
                return redirect(reverse('admin:houses_house_changelist'))
        else:
            form = MeterReadingForm()
        return render(request, 'admin/houses/house/meter_reading.html', {'form': form, 'house': house})

    def update_rent_view(self, request, pk):
        house = self.get_object(request, pk)
        if request.method == 'POST':
            form = RentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('admin:houses_house_changelist'))
        else:
            form = RentForm()
        return render(request, 'admin/houses/house/update_rent.html', {'form': form, 'house': house})


admin.site.register(House, HouseAdmin)
admin.site.register(Payment)
admin.site.register(MeterReading)
