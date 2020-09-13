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
        fields =('name','difficulty_level','description','average_class_size','price')