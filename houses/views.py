from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import House, MeterReading
from .forms import HouseForm, RentForm, MeterReadingForm


class HouseListView(LoginRequiredMixin, ListView):
    model = House
    template_name = 'houses/house_list.html'
    context_object_name = 'houses'
    ordering = ['name']


class HouseDetailView(LoginRequiredMixin, DetailView):
    model = House
    template_name = 'houses/house_detail.html'
    context_object_name = 'house'


class HouseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = House
    form_class = HouseForm
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('houses:house_list')
    success_message = 'House successfully created.'


class HouseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = House
    form_class = HouseForm
    template_name = 'houses/house_form.html'
    success_url = reverse_lazy('houses:house_list')
    success_message = 'House successfully updated.'


class MeterReadingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = MeterReading
    form_class = MeterReadingForm
    template_name = 'houses/meter_reading_form.html'
    success_url = reverse_lazy('houses:house_list')
    success_message = 'Meter reading successfully updated.'

    def form_valid(self, form):
        form.instance.current_reading -= form.instance.previous_reading
        return super().form_valid(form)


class RentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = House
    form_class = RentForm
    template_name = 'houses/rent_form.html'
    success_url = reverse_lazy('houses:house_list')
    success_message = 'Rent successfully updated.'


    def get_initial(self):
        initial = super().get_initial()
        house = self.get_object()
        initial['rent'] = house.rent_amount
        return initial
