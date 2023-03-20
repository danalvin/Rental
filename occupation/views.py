from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, F, ExpressionWrapper, fields

from houses.models import House
from .models import Occupation, Payment

class OccupationListView(LoginRequiredMixin, ListView):
    model = Occupation
    context_object_name = 'occupations'
    template_name = 'occupation/occupation_list.html'
    ordering = ['-move_in_date']

class OccupationDetailView(LoginRequiredMixin, DetailView):
    model = Occupation
    context_object_name = 'occupation'
    template_name = 'occupation/occupation_detail.html'

class OccupationCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Occupation
    fields = ['tenant', 'house', 'move_in_date', 'rent_due_date']
    template_name = 'occupation/occupation_form.html'
    success_url = reverse_lazy('occupation_list')
    success_message = "Occupation was created successfully."

    def form_valid(self, form):
        house = form.cleaned_data['house']
        if Occupation.objects.filter(house=house, move_out_date__isnull=True).exists():
            messages.error(self.request, f"{house} is already occupied.")
            return self.form_invalid(form)
        return super().form_valid(form)

class OccupationUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Occupation
    fields = ['tenant', 'house', 'move_in_date', 'rent_due_date']
    template_name = 'occupation/occupation_form.html'
    success_url = reverse_lazy('occupation_list')
    success_message = "Occupation was updated successfully."

    def form_valid(self, form):
        house = form.cleaned_data['house']
        if Occupation.objects.filter(house=house, move_out_date__isnull=True).exclude(pk=self.object.pk).exists():
            messages.error(self.request, f"{house} is already occupied.")
            return self.form_invalid(form)
        return super().form_valid(form)

class OccupationDeleteView(LoginRequiredMixin, DeleteView):
    model = Occupation
    success_url = reverse_lazy('occupation_list')
    template_name = 'occupation/occupation_confirm_delete.html'

class PaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    fields = ['occupation', 'amount', 'payment_date']
    template_name = 'occupation/payment_form.html'
    success_url = reverse_lazy('occupation_list')
    success_message = "Payment was created successfully."

    def get_initial(self):
        occupation_id = self.kwargs.get('pk')
        occupation = get_object_or_404(Occupation, pk=occupation_id)
        return {'occupation': occupation}

    def form_valid(self, form):
        occupation = form.cleaned_data['occupation']
        rent = occupation.house.rent
        amount = form.cleaned_data['amount']
        if amount < rent:
            messages.error(self.request, f"Payment amount must be at least {rent}.")
            return self.form_invalid(form)
        return super().form_valid(form)

class PaymentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    fields = ['amount', 'payment_date']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('payment-list')
    success_message = "Payment successfully updated."

    def get_initial(self):
        initial = super().get_initial()
        initial['tenant'] = self.object.occupation.tenant.id
        initial['occupation'] = self.object.occupation.id
        return initial