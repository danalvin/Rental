from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings

from houses.models import House
from .models import Tenant, Occupation, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'occupation', 'amount', 'payment_date')
    list_filter = ('payment_date',)
    search_fields = ('tenant__full_name', 'occupation__house__house_number')

class OccupationAdmin(admin.ModelAdmin):
    list_display = ('house', 'tenant', 'rent_amount', 'rent_due_date', 'rent_status')
    list_filter = ('rent_status',)
    search_fields = ('house__house_number', 'tenant__full_name')
    actions = ['send_rent_due_reminder_email']

    def send_rent_due_reminder_email(self, request, queryset):
        for occupation in queryset:
            tenant_email = occupation.tenant.email
            subject = f'Rent Due Reminder for {occupation.house.house_number}'
            message = f'Dear {occupation.tenant.full_name},\n\nThis is a reminder that the rent for {occupation.house.house_number} is due on {occupation.rent_due_date}. Please ensure that payment is made on or before the due date.\n\nThank you.'
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, from_email, [tenant_email])
        self.message_user(request, 'Rent due reminder email sent successfully.')
    send_rent_due_reminder_email.short_description = 'Send rent due reminder email to selected tenants'

class TenantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'id_number')

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class OccupationInline(admin.TabularInline):
    model = Occupation
    extra = 0
    readonly_fields = ['rent_due_date', 'rent_status']

class HouseAdmin(admin.ModelAdmin):
    list_display = ('house_number', 'house_name', 'water_meter_reading', 'rent_amount', 'rent_status')
    inlines = [OccupationInline, PaymentInline]
    search_fields = ('house_number', 'house_name')
    actions = ['send_water_meter_reading_reminder_email']

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

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(House, HouseAdmin)
