from django.db import models
from tenant.models import tenant

# Create your models here.

class house(models.Model):
    housenumber = models.PositiveIntegerField(unique=True, )
    # tenant = models.ForeignKey(on_delete=models.DO_NOTHING, to=tenant)
    # Water = models.PositiveIntegerField()
    # internet_subscription = models.PositiveIntegerField()
    rent = models.PositiveIntegerField()

    def __str__(self):
        return self.housenumber




# send message - {{ occupation.tenant.phonenumber }}, of house number {{ occupation.house.housenumber }}, of pending rent bill of ksh 
# {{ occupation.house.rent }}, water utility bill of ({{ occupation.water.current_reading }} - {{ occupation.water.previous_reading }} * 100) and internet usage of {{ occupation.wifi.speed }} of 
# {{ occupation.wifi.price }} please make a payment to this number. 
