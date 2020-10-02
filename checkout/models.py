from django.db import models
from customers.models import Customer
from lessons.models import Lesson
from products.models import Product
# Create your models here.
class Lesson_Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    price = models.PositiveIntegerField(blank=False)
    purchase_date = models.DateTimeField(blank=False,auto_now=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)

    def __str__(self):
        return f"Purchase made for id: {self.lesson.id} by {self.customer.user.username}" \
               f" on {self.purchase_date}"

class Product_Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    total_cost = models.PositiveIntegerField(blank=False)
    purchase_date = models.DateTimeField(blank=False,auto_now=True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False,default=0)
    price = models.PositiveIntegerField(blank=False,default=0)

    def __str__(self):
        return f"Purchase made for id:{self.product.id} by {self.customer.user.username}" \
               f" on {self.purchase_date}"

    # Overriding the default save
    def save(self, *args, **kwargs):
        self.total_cost  = self.price * self.quantity
        super().save(*args,**kwargs)