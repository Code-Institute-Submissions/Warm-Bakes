from django.shortcuts import render,redirect,get_object_or_404,reverse
from .models import Lesson_Review, Product_Review
from .forms import LessonReviewForm,ProductReviewForm
from products.models import Product
from lessons.models import Lesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
@login_required
def user_reviews(request):
    product_reviews = Product_Review.objects.filter(buyer=request.user)
    lesson_reviews = Lesson_Review.objects.filter(user_attendee=request.user)
    return render(request,'reviews/view_all_reviews.template.html',{
        'product_reviews':product_reviews,
        'lesson_reviews':lesson_reviews
    })

@login_required
def create_product_review(request,product_id):
    product_reviewed = get_object_or_404(Product,pk=product_id)
    if request.method =='POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review_model= review_form.save(commit=False)
            review_model.product_bought=product_reviewed
            review_model.buyer=request.user
            review_model.save()
            messages.success(request,"New Review has been added successfully")
            return redirect(reverse('show_product_detail_route',kwargs={'product_id':product_id}))
    else:
        review_form=ProductReviewForm()
        return render(request,'reviews/create_product_review.template.html',{
            'form':review_form,
            'product':product_reviewed
        })

@login_required
def create_lesson_review(request,lesson_id):
    lesson_reviewed=get_object_or_404(Lesson,pk=lesson_id)
    if request.method =='POST':
        review_form = LessonReviewForm(request.POST)
        if review_form.is_valid():
            review_model=review_form.save(commit=False)
            review_model.class_attended=lesson_reviewed
            review_model.user_attendee=request.user
            review_model.save()
            messages.success(request,'New Review has been added successfully')
            return redirect(reverse('show_lesson_details_route',kwargs={'lesson_id':lesson_id}))
    else:
        review_form = LessonReviewForm()
        return render(request,'reviews/create_lesson_review.template.html',{
            'form':review_form,
            'lesson':lesson_reviewed,
        })

@login_required
def update_product_review(request,product_review_id):
    product_to_update = get_object_or_404(Product_Review,pk=product_review_id)

    if request.method == "POST":
        product_review_form = ProductReviewForm(request.POST, instance=product_to_update)

        if product_review_form.is_valid():
            product_review_form.save()
            messages.success(request,"Review has been updated successfully")
            return redirect(reverse('view_all_reviews_route'))
        else:
            product_review_form = ProductReviewForm(instance=product_to_update)
            return render(request, 'reviews/update_product_review.template.html',{
                "form": product_review_form
            })

    else:
        product_review_form = ProductReviewForm(instance=product_to_update)
        return render(request,'reviews/update_product_review.template.html',{
            'form':product_review_form
        })


@login_required
def update_lesson_review(request,lesson_id):
    lesson_to_update = get_object_or_404(Lesson_Review,pk=lesson_id)

    if request.method == "POST":
        lesson_review_form = LessonReviewForm(request.POST, instance=lesson_to_update)

        if lesson_review_form.is_valid():
            lesson_review_form.save()
            messages.success(request,"Review has been updated successfully")
            return redirect(reverse('view_all_reviews_route'))
        else:
            lesson_review_form = LessonReviewForm(instance=lesson_to_update)
            return render(request, 'review/update_lesson_review.template.html',{
                "form": lesson_review_form
            })

    else:
        lesson_review_form = LessonReviewForm(instance=lesson_to_update)
        return render(request,'review/update_lesson_review.template.html',{
            'form':lesson_review_form
        })

@login_required
def delete_lesson_review(request,product_id):
    product_to_delete = get_object_or_404(Product,pk=product_id)
    if request.method =="POST":
        product_to_delete.delete()
        messages.success(request,f"Product {product_to_delete.name} has been deleted")
        return redirect(products_inventory)
    else:
        return render(request,'products/delete_product.template.html',{
            'product':product_to_delete
        })
