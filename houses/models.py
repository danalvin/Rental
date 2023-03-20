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