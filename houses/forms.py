from django import forms
from .models import House, MeterReading


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = '__all__'


class RentForm(forms.Form):
    amount = forms.DecimalField()
    date_due = forms.DateField()
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), required=False)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Rent amount must be greater than zero.')
        return amount
    
    def clean_date_due(self):
        date_due = self.cleaned_data.get('date_due')
        if date_due < self.initial['date_issued']:
            raise forms.ValidationError('Due date cannot be before the date of issue.')
        return date_due


class MeterReadingForm(forms.ModelForm):
    class Meta:
        model = MeterReading
        fields = ('house', 'current_reading', 'reading_date')
        
    def clean_reading(self):
        house = self.cleaned_data.get('house')
        reading = self.cleaned_data.get('current_reading')
        if current_reading < house.previous_reading:
            raise forms.ValidationError('Meter reading cannot be less than the previous reading.')
        return current_reading
