from django.test import TestCase
from django.contrib.auth.models import User
from lessons.models import Lesson,Difficulty
from products.models import Product,Category
from .models import Lesson_Review,Product_Review
from django.shortcuts import reverse

#Create your tests here.
class TestReviewsViews(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='testuser123',password='rotiprata963')
        self.client.login(username='testuser123',password='rotiprata963')
    def test_get_user_my_reviews_page(self):
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'reviews/view_all_reviews.template.html')
class TestReviewsForms(TestCase):
    def setUp(self):
        # Create the model instances required for the relationship
        self.new_difficulty = Difficulty(name="Very Tough")
        self.new_difficulty.save()

        self.new_category = Category(name="Solid Cakes")
        self.new_category.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level":self.new_difficulty,
            "description": "Good Stuff",
        }
        product_raw_data = {
            "name": "Fairy Cake",
            "price": 3000,
            "category":self.new_category,
            "description": "Great Cake!",
            "sizes": "S"
        }
        #Pass the dictionary as named parameters to a function call
        self.new_lesson = Lesson(**raw_data)
        self.new_lesson.save()

        self.new_product = Product(**product_raw_data)
        self.new_product.save()

        self.user=User.objects.create_user(username='testuser123',password='rotiprata963')
        self.client.login(username='testuser123',password='rotiprata963')
    
    def test_get_create_lesson_review_page(self):
        response = self.client.get(f'/reviews/create/{self.new_lesson.id}')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'reviews/create_lesson_review.template.html')

    def test_create_lesson_review(self):
        raw_data = {
            'title': 'Not Good Lesson!',
            'content': 'Waste Time!',
            'ratings': 1
        }
        response = self.client.post(f'/reviews/create/{self.new_lesson.id}',raw_data)
        self.assertEqual(response.status_code,302)
        new_review = Lesson_Review.objects.get(title="Not Good Lesson!")
        self.assertNotEqual(new_review, None)
        self.assertEqual(new_review.title , raw_data["title"])
        self.assertEqual(new_review.content, raw_data["content"])
        self.assertEqual(new_review.ratings, raw_data["ratings"])

    def test_get_create_product_review_page(self):
        response = self.client.get(reverse('create_product_review_route',kwargs={'product_id':str(self.new_product.id)}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'reviews/create_product_review.template.html')

    def test_create_product_review(self):
        raw_data = {
            'title': 'Good Cake!',
            'content': 'Worth Every Penny!',
            'ratings': 5
        }
        response = self.client.post(reverse('create_product_review_route',kwargs={'product_id':str(self.new_product.id)}),raw_data)
        print(response.content)
        self.assertEqual(response.status_code,302)
        new_review = Product_Review.objects.get(title="Good Cake!")
        self.assertNotEqual(new_review, None)
        self.assertEqual(new_review.title , raw_data["title"])
        self.assertEqual(new_review.content, raw_data["content"])
        self.assertEqual(new_review.ratings, raw_data["ratings"])


