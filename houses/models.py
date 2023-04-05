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
    current_reading = models.DecimalField(max_digits=10, decimal_places=2)
    consumption = models.PositiveIntegerField()
    cost = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.house.house_name} - {self.reading_date}"

    def save(self, *args, **kwargs):
        # Calculate consumption and update previous reading
        house = self.house
        if self.pk is None:
            # This is a new object being saved for the first time
            self.consumption = self.current_reading - house.water_meter_reading
            self.cost = self.consumption * 150
            house.water_meter_reading = self.current_reading
        else:
            # This is an existing object being updated
            last_reading = MeterReading.objects.filter(house=self.house).exclude(pk=self.pk).order_by('-reading_date').first()
            if last_reading:
                self.consumption = self.current_reading - last_reading.current_reading
            else:
                self.consumption = self.current_reading - house.water_meter_reading
            self.cost = self.consumption * 150
        house.save()

        # Call the original save method to save the object to the database
        super().save(*args, **kwargs)


class Rent(models.Model):
    tenant = models.ForeignKey(tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='rented')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.amount}"
