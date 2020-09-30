from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Customer

class CustomizedSignupForm(SignupForm):
    contact_number =PhoneNumberField(required=True)
    address = forms.CharField(max_length=100,required=True)
    postal_code = forms.IntegerField(required=True)

    def save(self,request):
        user = super(CustomizedSignupForm,self).save(request)

        customer = Customer()
        customer.contact_number = self.cleaned_data['contact_number']
        customer.address = self.cleaned_data['address']
        customer.postal_code = self.cleaned_data['postal_code']
        customer.user = user
        customer.save()

        return user 

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('contact_number','address','postal_code')