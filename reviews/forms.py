from .models import Product_Review, Lesson_Review
from django import forms

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = Product_Review
        fields =('title','content','ratings')
        exclude =('buyer','product_bought')


class LessonReviewForm(forms.ModelForm):
    class Meta:
        model=Lesson_Review
        fields =('title','content','ratings')
        exclude =('user_attendee','classes_attended')