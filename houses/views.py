from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import MeterReading
from .forms import MeterReadingForm


from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import House, MeterReading
from .forms import MeterReadingForm

class HouseListView(ListView):
    model = House
    template_name = 'houses/house_list.html'

class HouseDetailView(DetailView):
    model = House
    template_name = 'houses/house_detail.html'

class HouseUpdateView(UpdateView):
    model = House
    fields = ['rent_amount', 'rent_due_date', 'rent_status']
    template_name = 'houses/house_update.html'

# class MeterReadingUpdateView(UpdateView):
#     model = MeterReading
#     form_class = MeterReadingForm
#     template_name = 'houses/meter_reading_update.html'

#     def form_valid(self, form):
#         house = get_object_or_404(House, pk=self.kwargs['pk'])
#         meter_reading = form.save(commit=False)
#         meter_reading.house = house
#         meter_reading.previous_reading = house.current_reading
#         meter_reading.consumption = meter_reading.current_reading - house.current_reading
#         house.current_reading = meter_reading.current_reading
#         house.save()
#         meter_reading.save()
#         return redirect('houses:house_detail', pk=house.pk)


class UpdateMeterReadingView(View):
    template_name = 'occupation/meter_reading.html'

    def get(self, request, house_id):
        house = get_object_or_404(House, pk=house_id)
        latest_reading = MeterReading.objects.filter(house=house).latest('reading_date')
        form = MeterReadingForm(instance=latest_reading)
        context = {'form': form, 'house': house}
        return render(request, self.template_name, context)

    def post(self, request, house_id):
        house = get_object_or_404(House, pk=house_id)
        latest_reading = MeterReading.objects.filter(house=house).latest('reading_date')
        form = MeterReadingForm(request.POST, instance=latest_reading)
        if form.is_valid():
            meter_reading = form.save(commit=False)
            meter_reading.house = house
            meter_reading.save()
            messages.success(request, "Meter reading updated successfully.")
            return redirect('home')
        context = {'form': form, 'house': house}
        return render(request, self.template_name, context)
