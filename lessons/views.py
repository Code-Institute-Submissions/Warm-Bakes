from django.shortcuts import render,redirect,reverse,get_object_or_404
from .models import Difficulty,Lesson
from .forms import DifficultyForm, LessonForm

def show_all_classes(request):
    return render(request,'lessons/show_all_classes.template.html')

def lessons_database(request):
    if request.method =="POST":
        difficulty_form = DifficultyForm(request.POST)
        if difficulty_form.is_valid():
            difficulty_form.save()
            return redirect(reverse(lessons_database))
        else:
            return redirect(reverse(lessons_database))
    else:
        difficulty = Difficulty.objects.all()
        lessons = Lesson.objects.all()
        difficulty_form = DifficultyForm()
        return render(request,'lessons/lessons_database.template.html',{
            'form': difficulty_form,
            'lessons': lessons,
            'difficulties':difficulty
        })

def delete_difficulty(request,difficulty_id):
    difficulty_to_delete = get_object_or_404(Difficulty,pk=difficulty_id)
    difficulty_to_delete.delete()
    return redirect(lessons_database)


def create_lesson(request):
    if request.method =='POST':
        lesson_form = LessonForm(request.POST)
        # Validate form fields
        if lesson_form.is_valid():
            lesson_form.save()
            return redirect(lessons_database)
        else:
            return render(request,'lessons/create_lesson.template.html',{
                'form':lesson_form
            })
    else:
        lesson_form = LessonForm()
        return render(request,'lessons/create_lesson.template.html',
        {
            'form':lesson_form
        })

def update_lesson(request,lesson_id):
    lesson_to_update = get_object_or_404(Lesson,pk=lesson_id)

    if request.method == "POST":
        lesson_form = LessonForm(request.POST, instance=lesson_to_update)

        if lesson_form.is_valid():
            lesson_form.save()
            return redirect(lessons_database)
        else:
            return render(request, 'lessons/update_lesson.template.html',{
                "form": lesson_form
            })

    else:
        lesson_form = LessonForm(instance=lesson_to_update)
        return render(request,'lessons/update_lesson.template.html',{
            'form':lesson_form
        })

def delete_lesson(request,lesson_id):
    lesson_to_delete = get_object_or_404(Lesson,pk=lesson_id)
    if request.method =="POST":
        lesson_to_delete.delete()
        return redirect(lessons_database)
    else:
        return render(request,'lessons/delete_lesson.template.html',{
            'lesson':lesson_to_delete
        })

def show_lesson_detail(request,lesson_id):
    lesson_being_viewed = get_object_or_404(Lesson,pk=lesson_id)
    return render(request,'lessons/show_lesson_detail.template.html',{
        'lesson': lesson_being_viewed
    })