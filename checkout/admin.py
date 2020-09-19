from django.contrib import admin

from .models import Lesson_Order, Product_Order
# Register your models here.
admin.site.register(Lesson_Order)
admin.site.register(Product_Order)