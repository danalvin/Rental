from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from datetime import timezone
from django.core.mail import send_mail
import africastalking

africastalking.initialize('sandbox', '56dcc2bbb99125c299583f286a9355279b280d3830dfcbe6363534f7c8110de6')


def send_sms(message, recipients):
    sms = africastalking.SMS
    response = sms.send(message, recipients)
    return response


from houses.forms import MeterReadingForm, RentForm

from .models import House, Rent, MeterReading


class RentInline(admin.TabularInline):
    model = Rent
    extra = 1



class HouseAdmin(admin.ModelAdmin):
    inlines = [RentInline]
    list_display = ('house_name', 'rent_status', 'water_meter_reading')
    list_filter = ('rent',)
    search_fields = ('house_name', 'address')
    actions = ('send_water_meter_reading_reminder_email', 'send_water_meter_reading_reminder_text')

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

    def send_water_meter_reading_reminder_email(self, request, queryset):
        for house in queryset:
            occupation_set = house.occupation_set.all()
            for occupation in occupation_set:
                tenant_email = occupation.tenant.email
                subject = f'Water Meter Reading Reminder for {house.house_number}'
                message = f'Dear {occupation.tenant.full_name},\n\nThis is a reminder to submit the water meter reading for {house.house_number}. Please submit the water meter reading as soon as possible.\n\nThank you.'
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [tenant_email])
        self.message_user(request, 'Water meter reading reminder email sent successfully.')
    send_water_meter_reading_reminder_email.short_description = 'Send water meter reading reminder email to selected tenants'
    
    
    def send_water_meter_reading_reminder_text(self, request, queryset):
        for house in queryset:
            occupation_set = house.occupation_set.all()
            for occupation in occupation_set:
                tenant_phone = occupation.tenant.Phone_number
                message = f'Dear {occupation.tenant.full_name},\n\nThis is a reminder to submit the water meter reading and rent for {house.house_number}. Please submit the water meter reading as soon as possible.\n\nThank you.'
                recipients = tenant_phone
                responce=send_sms(message, recipients)
        self.message_user(request, 'Water meter reading reminder email sent successfully.')
        print(responce)
    send_water_meter_reading_reminder_text.short_description = 'Send water meter reading reminder email to selected tenants'


class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('house_name', 'reading_date', 'previous_reading', 'current_reading', 'consumption')
    readonly_fields = ('consumption',)

    def house_name(self, obj):
        return obj.house.house_name
    house_name.admin_order_field = 'house__name'
    house_name.short_description = 'House Name'



from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_title = 'Rental management System'  # Change the title displayed in the browser tab
    site_header = 'Rental management System'  # Change the title displayed on the page
    index_title = 'Welcome to Beracah apartments rental management system'  # Change the welcome text displayed on the dashboard

admin.site.register(MeterReading, MeterReadingAdmin)

admin.site.register(House, HouseAdmin)
admin.site.register(Rent)