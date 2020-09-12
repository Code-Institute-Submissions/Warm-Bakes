from django.test import TestCase
from .models import *
from django.shortcuts import get_object_or_404
# Create your tests here.
class TestProductsViews(TestCase):

    def test_get_show_all_products(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'products/show_all_products.template.html')
    
    def test_get_show_current_inventory(self):
        response = self.client.get('/products/inventory/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'products/products_inventory.template.html')


class TestCategoryForm(TestCase):
    def test_can_create_category(self):
        self.client.post('/products/inventory/',{
            'name':'Chocolate Cakes'
        })
        category = Category.objects.filter(name='Chocolate Cakes')
        self.assertEqual(category.count(),1)

    def test_can_delete_category(self):
        new_category = Category(name='Butter Cakes')
        new_category.save()
        check_category = Category.objects.filter(name='Butter Cakes')
        response = self.client.get(f'/products/category/delete/{new_category.id}')
        self.assertEqual(response.status_code,302)
        self.assertEqual(check_category.count(),0,"Deleted Category from database")

class TestProductsForm(TestCase):
    
    def test_get_create_product_form(self):
        response = self.client.get('/products/create/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'products/create_product.template.html')
    
    def test_create_product_form(self):
        # Create the model instances required for the relationship
        new_category = Category(name="Solid Cakes")
        new_category.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Red Velvet Cake",
            "price": 3000,
            "category": str(new_category.id),
            "description": "Good Stuff",
            "sizes":"M"
        }

        response =self.client.post('/products/create/', raw_data)

        self.assertEqual(response.status_code,302)
        # Find product with the name combo
        new_product = Product.objects.get(name="Red Velvet Cake")
        self.assertNotEqual(new_product, None)
        self.assertEqual(new_product.name , raw_data["name"])
        self.assertEqual(new_product.price, raw_data["price"])
        self.assertEqual(str(new_product.category.id), raw_data["category"])
        self.assertEqual(new_product.description,raw_data["description"])
        self.assertEqual(new_product.sizes,raw_data["sizes"])



    def test_get_edit_product_form(self):
        new_category = Category(name="Solid Cakes")
        new_category.save()
        
        raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category": new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        new_product = Product(**raw_data)
        new_product.save()

        # Display the edit form
        response = self.client.get(f'/products/edit/{new_product.id}')

        # assert route is rendered correctly with the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'products/update_product.template.html')

        # assert that each of the individual fields are in the form
        for key, data in raw_data.items():
            self.assertContains(response,str(data))
    
    
    def test_edit_product_form(self):
        new_category = Category(name="Solid Cakes")
        new_category.save()
        
        raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category":new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        new_product = Product(**raw_data)
        new_product.save()

        #Create the data to be changed
        category2 = Category(name="Rock Solid Cakes")
        category2.save()

        modified_data = {
            "name": "Bad Fairy Cake",
            "price": 5000,
            "category": str(category2.id),
            "description": "Not so bad after all!",
            "sizes": "L"
        } 

        #send the response and make sure the page is redirected
        response = self.client.post(f'/products/edit/{new_product.id}',modified_data)
        print(response.content)
        self.assertEqual(response.status_code,302)

        #Retrieve the product from the database and see if it has been modified
        modified_product = get_object_or_404(Product, pk=new_product.id)
        modified_data['category'] = category2
        for key, data in modified_data.items():
            self.assertEquals(getattr(modified_product,key),data) 

    def test_get_delete_product_form(self):
        # Create the model instances required for the relationships
        new_category = Category(name="Solid Cakes")
        new_category.save()
        
        raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category":new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        #Pass the dictionary as named parameters to a function call
        new_product = Product(**raw_data)
        new_product.save()

        #Assert route is rendered correctly and with the correct template
        response = self.client.get(f'/products/delete/{new_product.id}')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'products/delete_product.template.html')

    def test_actual_delete_product(self):
        # Create the model instances required for the relationships
        new_category = Category(name="Solid Cakes")
        new_category.save()
        
        raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category":new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        #Pass the dictionary as named parameters to a function call
        new_product = Product(**raw_data)
        new_product.save()

        #Perform the actual delete
        response = self.client.post(f'/products/delete/{new_product.id}')
        self.assertEqual(response.status_code,302)

        #Check if the product has been deleted
        deleted_product = Product.objects.filter(pk=new_product.id).first()
        self.assertEquals(deleted_product,None)




