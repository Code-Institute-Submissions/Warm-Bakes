from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Difficulty(models.Model):
    name= models.CharField(max_length=255,blank=False)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255,blank=False)
    difficulty_level = models.ForeignKey(Difficulty,on_delete=models.SET_NULL,null=True)
    description = models.TextField(blank=False)
    average_class_size = models.PositiveIntegerField(blank=False)
    price = models.PositiveIntegerField(blank=False)
    image = CloudinaryField(blank=True,null=True)


    def __str__(self):
        return self.name

    
