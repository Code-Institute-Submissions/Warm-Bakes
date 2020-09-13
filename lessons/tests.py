from django.test import TestCase
from .models import Difficulty,Lesson
from django.shortcuts import get_object_or_404
# Create your tests here.
class TestLessonsViews(TestCase):
    def test_get_show_all_classes(self):
        response =self.client.get('/lessons/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lessons/show_all_classes.template.html')
    
    def test_get_show_lessons_database(self):
        response=self.client.get('/lessons/database/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lessons/lessons_database.template.html')

    def test_get_show_lesson_detail(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": new_difficulty,
            "description": "Good Stuff",
        }
        new_lesson = Lesson(**raw_data)
        new_lesson.save()

        #Assert route is rendered correctly and with the correct template
        response = self.client.get(f'/lessons/detail/{new_lesson.id}')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lessons/show_lesson_detail.template.html')



class TestDiificultyForm(TestCase):
    def test_can_create_difficulty(self):
        self.client.post('/lessons/database/',{
            'name':'Ultra Difficult'
        })
        difficulty = Difficulty.objects.filter(name='Ultra Difficult')
        self.assertEqual(difficulty.count(),1)

    def test_can_delete_difficulty(self):
        new_difficulty = Difficulty(name='Very Difficult')
        new_difficulty.save()
        check_difficulty = Difficulty.objects.filter(name='Very Difficult')
        response = self.client.get(f'/lessons/difficulty/delete/{new_difficulty.id}')
        self.assertEqual(response.status_code,302)
        self.assertEqual(check_difficulty.count(),0,"Deleted Category from database")
    
class TestLessonsForm(TestCase):
    def test_can_get_lesson_form(self):
        response = self.client.get('/lessons/create/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lessons/create_lesson.template.html')
    
    def test_can_post_lesson_form(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": str(new_difficulty.id),
            "description": "Good Stuff",
        }

        response =self.client.post('/lessons/create/', raw_data)

        self.assertEqual(response.status_code,302)
        # Find product with the name combo
        new_lesson = Lesson.objects.get(name="Cherry Cake")
        self.assertNotEqual(new_lesson, None)
        self.assertEqual(new_lesson.name , raw_data["name"])
        self.assertEqual(new_lesson.price, raw_data["price"])
        self.assertEqual(str(new_lesson.difficulty_level.id), raw_data["difficulty_level"])
        self.assertEqual(new_lesson.description,raw_data["description"])
        self.assertEqual(new_lesson.average_class_size,raw_data["average_class_size"])


    def test_can_get_edit_lesson_form(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": new_difficulty,
            "description": "Good Stuff",
        }
        new_lesson = Lesson(**raw_data)
        new_lesson.save()

        # Display the edit form
        response = self.client.get(f'/lessons/edit/{new_lesson.id}')

        # assert route is rendered correctly with the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'lessons/update_lesson.template.html')

        # assert that each of the individual fields are in the form
        for key, data in raw_data.items():
            self.assertContains(response,str(data))

    def test_can_post_edit_lesson_form(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": new_difficulty,
            "description": "Good Stuff",
        }
        new_lesson = Lesson(**raw_data)
        new_lesson.save()


        #Create the data to be changed
        difficulty2 = Difficulty(name="Easy Peazy")
        difficulty2.save()

        modified_data = {
            "name": "A lot of Cherry Cake",
            "price": 5000,
            "average_class_size":50,
            "description": "Not so bad!",
            "difficulty_level": str(difficulty2.id)
        } 

        #send the response and make sure the page is redirected
        response = self.client.post(f'/lessons/edit/{new_lesson.id}',modified_data)
        print(response.content)
        self.assertEqual(response.status_code,302)

        #Retrieve the lesson from the database and see if it has been modified
        modified_lesson = get_object_or_404(Lesson, pk=new_lesson.id)
        modified_data['difficulty_level'] = difficulty2
        for key, data in modified_data.items():
            self.assertEquals(getattr(modified_lesson,key),data) 

    def test_can_get_delete_lesson_form(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": new_difficulty,
            "description": "Good Stuff",
        }
        new_lesson = Lesson(**raw_data)
        new_lesson.save()

        #Assert route is rendered correctly and with the correct template
        response = self.client.get(f'/lessons/delete/{new_lesson.id}')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'lessons/delete_lesson.template.html')
    def test_can_post_delete_lesson_form(self):
        # Create the model instances required for the relationship
        new_difficulty = Difficulty(name="Very Tough")
        new_difficulty.save()
        # Create the raw data for testing
        raw_data = {
            "name":"Cherry Cake",
            "price": 3000,
            "average_class_size": 25,
            "difficulty_level": new_difficulty,
            "description": "Good Stuff",
        }
        new_lesson = Lesson(**raw_data)
        new_lesson.save()

        #Perform the actual delete
        response = self.client.post(f'/lessons/delete/{new_lesson.id}')
        self.assertEqual(response.status_code,302)

        #Check if the lesson has been deleted
        deleted_lesson = Lesson.objects.filter(pk=new_lesson.id).first()
        self.assertEquals(deleted_lesson,None)
