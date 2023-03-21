from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.conf import settings

from houses.models import House
from .models import Occupation, Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date', 'occupation_name')
    list_filter = ('date',)
    search_fields = ('tenant__full_name', 'occupation__house__house_number')

class OccupationAdmin(admin.ModelAdmin):
    list_display = ('house', 'tenant', 'rent_amount', 'rent_due_date')
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


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

class OccupationInline(admin.TabularInline):
    model = Occupation
    extra = 0
    readonly_fields = ['rent_due_date', 'rent_status']


admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Payment, PaymentAdmin)
