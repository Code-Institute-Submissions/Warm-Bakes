from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from lessons.models import Lesson
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here.

class Lesson_Review(models.Model):
    content= models.TextField(blank=False)
    ratings = GenericRelation(Rating,related_query_name='lessons_list')
    class_attended = models.ForeignKey(Lesson,on_delete=models.CASCADE,blank=False)
    user_attendee = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    date_posted = models.DateTimeField(blank=False,auto_now=True)

    def __str__(self):
        return self.user_attendee.username  + " " + self.date_posted

class Product_Review(models.Model):
    content = models.TextField(blank=False)
    ratings = GenericRelation(Rating,related_query_name='products_list')
    product_bought = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False)
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    date_posted = models.DateTimeField(blank=False,auto_now=True)

    def __str__(self):
        return self.buyer.username + " " + self.date_posted
