from django import forms
from .models import Category, Product
from cloudinary.forms import CloudinaryJsFileField

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ('name',)


class ProductForm(forms.ModelForm):
    image = CloudinaryJsFileField(required=False)
    class Meta:
        model = Product
        fields =('name','price','category','description','sizes')