from django.db import models
from cloudinary.models import CloudinaryField
import uuid
# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length=255,blank=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(max_length=255,blank=False)
    price = models.PositiveIntegerField(blank=False)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    description = models.TextField(blank=False)
    sizes = models.CharField(max_length=6,choices=(
        ('S','Small'),
        ('M','Medium'),
        ('L','Large')
    ),null=True,blank=True)
    image = CloudinaryField(blank=True,null=True)

    def __str__(self):
        return self.name
    
