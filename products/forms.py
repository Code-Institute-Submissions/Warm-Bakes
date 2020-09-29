from django import forms
from .models import Category, Product
from cloudinary.forms import CloudinaryJsFileField

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ('name',)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =('name','price','category','description','sizes','cover')
    cover = CloudinaryJsFileField(required=False)

ORDER = [
    ('Ascending','Sort In Ascending Order'),
    ('Descending','Sort In Descending Order')
]
class SearchForm(forms.Form):
    name = forms.CharField(max_length=100,required=False)
    category= forms.ModelChoiceField(queryset=Category.objects.all(),
    required=False)
    price = forms.ChoiceField(choices=ORDER,widget=forms.RadioSelect(attrs={'class': 'form-check-inline'}),required=False)
    



