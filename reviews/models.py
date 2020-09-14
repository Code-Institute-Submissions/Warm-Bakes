from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from lessons.models import Lesson
# Create your models here.

class Lesson_Review(models.Model):
    RATING_CHOICES= (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    )
    title = models.CharField(blank=False,max_length=255)
    content= models.TextField(blank=False)
    ratings = models.IntegerField(choices=RATING_CHOICES)
    class_attended = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=False)
    user_attendee = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    date_posted = models.DateTimeField(blank=False,auto_now=True)

    def __str__(self):
        return self.user_attendee.username  + " " + self.date_posted

class Product_Review(models.Model):
    RATING_CHOICES= (
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5')
    )
    title = models.CharField(blank=False,max_length=255)
    content = models.TextField(blank=False)
    ratings = models.IntegerField(choices=RATING_CHOICES)
    product_bought = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    date_posted = models.DateTimeField(blank=False,auto_now=True)

    def __str__(self):
        return self.buyer.username + " " + self.date_posted
