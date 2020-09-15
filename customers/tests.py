from django.test import TestCase
from .models import Customer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.test import Client
# Create your tests here.
class TestCustomerViews(TestCase):
    def get_user_profile_page(self):
        new_user = User(username="testuser123",
                        email="tester213@test.com")
        new_user.set_password('rotiprata963')
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
        
        new_client = Client()
        login_response =new_client.login(username="testuser123",password="rotiprata963")
        self.assertEqual(login_response.wsgi_request.user.is_authenticated,True) 

        response = new_client.get(f'/customers/myprofile/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'customers/show_profile.template.html')

class TestCustomerForm(TestCase):
    def get_edit_profile_page(self):
        new_user = User(username="testuser123",
                        email="tester213@test.com")
        new_user.set_password('rotiprata963')
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

        new_client = Client()
        login_response =new_client.login(username="testuser123",password="rotiprata963")
        self.assertEqual(login_response.wsgi_request.user.is_authenticated,True)
    
        #Assert route is rendered correctly and with the correct template
        response = new_client.get(f'/customers/myprofile/update/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'customers/update_profile.template.html')
    
    def test_edit_profile(self):
        new_user = User(username="testuser123",
                        email="tester213@test.com")
        new_user.set_password('rotiprata963')
        new_user.save()
        raw_data = {
            "user":new_user,
            "contact_number":"+6512345678",
            "address": "Block 991 Yishun Ring Road",
            "postal_code": 999999
        }
        #Pass the dictionary as named parameters to a function call
        new_customer = Customer(**raw_data)
        new_customer.save()
       
        new_client = Client()
        login_response =new_client.login(username="testuser123",password="rotiprata963")

        #Create the data to be changed
        modified_data = {
            "contact_number":"+6587654321",
            "address": "Block 451 Black Ring Road",
            "postal_code": 231456
        } 
        
        #send the response and make sure the page is redirected
        response = new_client.post(f'/customers/myprofile/update/',modified_data)
        print(response.content)
        self.assertEqual(response.status_code,302)

        #Retrieve the lesson from the database and see if it has been modified
        modified_customer = get_object_or_404(Customer, pk=new_customer.id)
        for key, data in modified_data.items():
            self.assertEquals(getattr(modified_customer,key),data) 


    
