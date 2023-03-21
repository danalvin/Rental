from django.utils import timezone
from django.db import models
from houses.models import House
from tenant.models import tenant as Tenant


class Occupation(models.Model):
    tenant_name = models.CharField(max_length=50)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    rent_due_date = models.DateField()
    occupation_start_date = models.DateField()

    def __str__(self):
        return self.tenant_name
    

class Occupation(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    rent_due_date = models.DateField(blank=True, null=True)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    occupied = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tenant} - {self.house} ({self.start_date} to {self.rent_due_date})"
    

class Vacation(models.Model):
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.occupation.tenant} - {self.occupation.house} ({self.start_date} to {self.end_date})"



class Payment(models.Model):
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.occupation.house.house_name} payment of {self.amount} on {self.date}"
    

    def occupation_name(self):
        return self.occupation.tenant