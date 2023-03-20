from django.db import models
from houses.models import House


class Occupation(models.Model):
    tenant_name = models.CharField(max_length=50)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    rent_due_date = models.DateField()
    occupation_start_date = models.DateField()

    def __str__(self):
        return self.tenant_name
    
class MeterReading(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    current_reading = models.IntegerField()
    previous_reading = models.IntegerField()
    reading_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.house} - {self.current_reading} - {self.reading_date}"
