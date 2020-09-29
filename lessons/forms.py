from django import forms
from .models import Difficulty, Lesson
from cloudinary.forms import CloudinaryJsFileField

class DifficultyForm(forms.ModelForm):
    class Meta:
        model = Difficulty
        fields= ('name',)

class LessonForm(forms.ModelForm):
    image = CloudinaryJsFileField(required=False)
    class Meta:
        model = Lesson
        fields =('name','difficulty_level','description','average_class_size','price','image')

ORDER = [
    ('Ascending','Sort In Ascending Order'),
    ('Descending','Sort In Descending Order')
]
class SearchForm(forms.Form):
    name = forms.CharField(max_length=100,required=False)
    difficulty= forms.ModelChoiceField(queryset=Difficulty.objects.all(),
    required=False)
    price = forms.ChoiceField(choices=ORDER,widget=forms.RadioSelect(attrs={'class': 'form-check-inline'}),required=False)