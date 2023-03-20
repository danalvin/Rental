from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Occupation, Payment

class OccupationForm(forms.ModelForm):
    class Meta:
        model = Occupation
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        occupation = cleaned_data.get('occupation')
        amount = cleaned_data.get('amount')
        if occupation and amount:
            if amount < occupation.rent:
                raise forms.ValidationError(_("Payment amount cannot be less than the rent."))
        return cleaned_data


class PaymentUpdateForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'date_paid', 'remarks']
    
    def __init__(self, *args, **kwargs):
        super(PaymentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['amount'].disabled = True
        self.fields['date_paid'].disabled = True
        self.fields['remarks'].initial = 'Update remarks here...'

