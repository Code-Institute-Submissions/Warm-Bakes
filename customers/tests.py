from django.test import TestCase
from .models import Customer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
# Create your tests here.
class TestCustomerViews(TestCase):
    def get_user_profile_page(self):
        response = self.client.get('/customers/myprofile')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'customers/show_profile.template.html')

class TestCustomerForm(TestCase):
    def get_edit_profile_page(self):
        raw_data = {
            "username": "testuser123",
            "password": "rotiprata963",
            "email":"tester213@test.com",
            "contact_number": "+6512345678",
            "address": "Block 991 Yishun Ring Road",
            "postal_code": "999999"
        }
        #Pass the dictionary as named parameters to a function call
        new_customer = Customer(**raw_data)
        new_customer.save()
    
        #Assert route is rendered correctly and with the correct template
        response = self.client.get(f'/customers/profile/update/{new_customer.id}')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'customers/update_profile.template.html')
    
    def test_edit_profile(self):
        new_user = User(username="testuser123",
                        password="rotiprata963",
                        email="tester213@test.com")
        new_user.save()
        raw_data = {
            "user":new_user,
            "contact_number": "+6512345678",
            "address": "Block 991 Yishun Ring Road",
            "postal_code": 999999
        }
        #Pass the dictionary as named parameters to a function call
        new_customer = Customer(**raw_data)
        new_customer.save()

        #Create the data to be changed
        modified_data = {
            "contact_number": "+6587654321",
            "address": "Block 451 Black Ring Road",
            "postal_code": 231456
        } 
        
        #send the response and make sure the page is redirected
        response = self.client.post(f'/customers/profile/update/{new_customer.id}',modified_data)
        print(response.content)
        self.assertEqual(response.status_code,302)

        #Retrieve the lesson from the database and see if it has been modified
        modified_customer = get_object_or_404(Customer, pk=new_customer.id)
        for key, data in modified_data.items():
            self.assertEquals(getattr(modified_customer,key),data) 


    
