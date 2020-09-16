from django.test import TestCase
from lessons.models import Difficulty, Lesson
from products.models import Product,Category
from django.shortcuts import reverse
# Create your tests here.
class TestCartViews(TestCase):
    def setUp(self):
        # Create the model instances required for the relationship
        self.new_difficulty = Difficulty(name="Very Tough")
        self.new_difficulty.save()

        self.new_category = Category(name="Solid Cakes")
        self.new_category.save()
        # Create the raw data for testing
        lesson_raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": self.new_difficulty,
            "description": "Good Stuff",
        }
        product_raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category":self.new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        self.new_lesson = Lesson(**lesson_raw_data)
        self.new_lesson.save()
        self.new_product = Product(**product_raw_data)
        self.new_product.save()
    
    def test_get_view_cart_page(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'cart/view_cart.template.html')
    
    def test_add_lesson_to_cart(self):
        response = self.client.get(f'/cart/add/{self.new_lesson.id}')
        session = self.client.session.get('lesson_shopping_cart')
        for k,v in session.items():
            lesson_added = v
        # Verify that the lesson has been added to cart
        self.assertEqual(lesson_added['id'],str(self.new_lesson.id))
        self.assertEqual(lesson_added['name'],self.new_lesson.name)
        self.assertEqual(lesson_added['cost'],'${:.2f}'.format(int(self.new_lesson.price/100)))

    def test_remove_lesson_from_cart(self):
        self.client.get(f'/cart/add/{self.new_lesson.id}')
        session = self.client.session.get('lesson_shopping_cart')
        for k,v in session.items():
            lesson_added = v
        # Check that the lesson has been added to the cart
        self.assertEqual(lesson_added['id'],str(self.new_lesson.id))
        self.assertEqual(lesson_added['name'],self.new_lesson.name)
        self.assertEqual(lesson_added['cost'],'${:.2f}'.format(int(self.new_lesson.price/100)))

        response=self.client.get(f'/cart/remove/{self.new_lesson.id}')
        #Check that lesson has been removed from the cart
        self.assertEqual(bool(self.client.session.get('lesson_shopping_cart')),False)

    def test_add_product_to_cart(self):
        response = self.client.get(reverse('add_product_to_cart_route',kwargs={'product_id':self.new_product.id}))
        session = self.client.session.get('product_shopping_cart')
        for k,v in session.items():
            product_added = v
        # Verify that the product has been added to cart
        self.assertEqual(product_added['id'],str(self.new_product.id))
        self.assertEqual(product_added['name'],self.new_product.name)
        self.assertEqual(product_added['cost'],'${:.2f}'.format(int(self.new_product.price/100)))
    
    def test_remove_product_from_cart(self):
        self.client.get(reverse('add_product_to_cart_route',kwargs={'product_id':self.new_product.id}))
        session = self.client.session.get('product_shopping_cart')
        for k,v in session.items():
            product_added = v
        # Check that the product has been added to cart
        self.assertEqual(product_added['id'],str(self.new_product.id))
        self.assertEqual(product_added['name'],self.new_product.name)
        self.assertEqual(product_added['cost'],'${:.2f}'.format(int(self.new_product.price/100)))
        self.assertEqual(product_added['qty'],1)

        response = self.client.post(reverse('remove_product_from_cart_route',kwargs={'product_id':self.new_product.id}))
        #Check that the product has been removed from the cart
        self.assertEqual(bool(self.client.session.get('product_shopping_cart')),False)

    def test_update_quantity_for_product(self):
        self.client.get(reverse('add_product_to_cart_route',kwargs={'product_id':self.new_product.id}))
        session = self.client.session.get('product_shopping_cart')
        for k,v in session.items():
            product_added = v
        # Verify that the product has been added to cart
        self.assertEqual(product_added['id'],str(self.new_product.id))
        self.assertEqual(product_added['name'],self.new_product.name)
        self.assertEqual(product_added['cost'],'${:.2f}'.format(int(self.new_product.price/100)))
        self.assertEqual(product_added['cost'],'${:.2f}'.format(int(self.new_product.price/100)))

        # Execute the update quantity view function
        response = self.client.post(reverse('update_product_quantity_to_cart_route',kwargs={'product_id':self.new_product.id}),{
            'qty':3
        })
        for k,v in self.client.session.get('product_shopping_cart').items():
            updated_product = v
        
        # Check that the quantity has been updated
        self.assertEqual(updated_product['qty'],str(3))
