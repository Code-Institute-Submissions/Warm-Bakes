from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = PhoneNumberField(null=False,blank=True,unique=True)
    address = models.CharField(max_length=100,null=True,blank=False)
    postal_code = models.PositiveIntegerField(unique=True,blank=False)
    def __str__(self):
        return self.user.username

