from django.db import models

# Create your models here.

class tenant(models.Model):
    First_name = models.CharField(max_length= 150)
    Second_name = models.CharField(max_length = 150)
    Phone_number = models.CharField(max_length=12)
    email = models.EmailField()
    ID_number = models.PositiveIntegerField()
    ID_front = models.FileField(upload_to= 'media', null=True)
    ID_back = models.FileField(upload_to= 'media', null=True)
    Signed_contract = models.FileField(upload_to= 'media', null=True)

    def __str__(self):
        return self.First_name