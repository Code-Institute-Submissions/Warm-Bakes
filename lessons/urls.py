from django.urls import path
import lessons.views

urlpatterns = [
    path('', lessons.views.show_all_classes,name="show_all_lessons_route"),
    path('database/',lessons.views.lessons_database, name="lessons_database_route"),
    path('difficulty/delete/<difficulty_id>',lessons.views.delete_difficulty,name="delete_difficulty_route"),
    path('create/',lessons.views.create_lesson,name="create_lesson_route"),
    path('edit/<lesson_id>',lessons.views.update_lesson,name="update_lesson_route"),
    path('delete/<lesson_id>',lessons.views.delete_lesson,name="delete_lesson_route"),
    path('detail/<lesson_id>',lessons.views.show_lesson_detail,name="show_lesson_details_route")
]