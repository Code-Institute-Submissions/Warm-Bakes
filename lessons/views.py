from django.shortcuts import render,redirect,reverse,get_object_or_404
from .models import Difficulty,Lesson
from .forms import DifficultyForm, LessonForm,SearchForm
from reviews.models import Lesson_Review
from django.contrib import messages
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required,login_required

def show_all_classes(request):
    all_lessons = Lesson.objects.all()

    #Check for queries submitted
    if request.GET:
        queries = ~Q(pk__in=[])

        #if a name is specified, add it to the query
        if 'name' in request.GET and request.GET['name']:
            name = request.GET['name']
            queries = queries & Q(name__icontains=name)

        #if a difficulty is specified, add it to the query
        if 'difficulty' in request.GET and request.GET['difficulty']:
            difficulty = request.GET['difficulty']
            queries= queries & Q(difficulty_level__in=difficulty)

        if 'price' in request.GET and request.GET['price']:
            selected = request.GET['price']
            if selected == 'Ascending':
                all_lessons = all_lessons.filter(queries).order_by('price')
            else:
                all_lessons = all_lessons.filter(queries).order_by('-price')


        #update the existing product found
        all_lessons= all_lessons.filter(queries)


    search_form = SearchForm(request.GET)
    return render(request,'lessons/show_all_classes.template.html',{
        'lessons':all_lessons,
        'search_form':search_form,
    })

@staff_member_required
@login_required
def lessons_database(request):
    if request.method =="POST":
        difficulty_form = DifficultyForm(request.POST)
           # Validate form fields
        if difficulty_form.is_valid():
            difficulty_form.save()
            messages.success(request,
            f"New Difficulty {difficulty_form.cleaned_data['name']} has been created")
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

@staff_member_required
@login_required
def delete_difficulty(request,difficulty_id):
    difficulty_to_delete = get_object_or_404(Difficulty,pk=difficulty_id)
    difficulty_to_delete.delete()
    messages.success(request,
    f"Difficulty {difficulty_to_delete.name} has been deleted")
    return redirect(lessons_database)

@staff_member_required
@login_required
def create_lesson(request):
    if request.method =='POST':
        lesson_form = LessonForm(request.POST)
        # Validate form fields
        if lesson_form.is_valid():
            lesson_form.save()
            messages.success(request,
            f"New Lesson {lesson_form.cleaned_data['name']} has been created")
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

@staff_member_required
@login_required
def update_lesson(request,lesson_id):
    lesson_to_update = get_object_or_404(Lesson,pk=lesson_id)

    if request.method == "POST":
        lesson_form = LessonForm(request.POST, instance=lesson_to_update)
           # Validate form fields
        if lesson_form.is_valid():
            lesson_form.save()
            messages.success(request,
            f"Lesson {lesson_form.cleaned_data['name']} has been updated")
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

@staff_member_required
@login_required
def delete_lesson(request,lesson_id):
    lesson_to_delete = get_object_or_404(Lesson,pk=lesson_id)
    if request.method =="POST":
        lesson_to_delete.delete()
        messages.success(request,
        f"Lesson {lesson_to_delete.name} has been deleted")
        return redirect(lessons_database)
    else:
        return render(request,'lessons/delete_lesson.template.html',{
            'lesson':lesson_to_delete
        })

def show_lesson_detail(request,lesson_id):
    lesson_being_viewed = get_object_or_404(Lesson,pk=lesson_id)
    reviews = Lesson_Review.objects.filter(class_attended=lesson_id)
    return render(request,'lessons/show_lesson_detail.template.html',{
        'lesson': lesson_being_viewed,
        'reviews':reviews
    })