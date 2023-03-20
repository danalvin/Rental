from django.utils import timezone
from django.db import models
from tenant.models import tenant

# Create your models here.

class House(models.Model):
    house_name = models.CharField(max_length=50)
    rent = models.DecimalField(max_digits=8, decimal_places=2)
    utilities = models.TextField()
    water_meter_reading = models.PositiveIntegerField(default=0)
    rent_status = models.BooleanField(default=False)

    def __str__(self):
        return self.house_name

    def update_rent_status(self):
        if self.rent_status == False and self.water_meter_reading > 0:
            self.rent_status = True
            self.save()

            
class MeterReading(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='meter_readings')
    reading_date = models.DateField(default=timezone.now)
    previous_reading = models.DecimalField(max_digits=10, decimal_places=2)
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.house.name} - {self.reading_date}"


class Rent(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='rented')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

class Payment(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE, related_name='test')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=timezone.now)