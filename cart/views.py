from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.contrib import messages
from lessons.models import Lesson
from products.models import Product
# Create your views here.
def add_lesson_to_cart(request,lesson_id):
    cart = request.session.get('lesson_shopping_cart',{})
    lesson = get_object_or_404(Lesson,pk=lesson_id)
    # Check if the lesson is in the cart
    if lesson_id not in cart:
        # add lesson to the cart
        cart[lesson_id] = {
            'id':lesson_id,
            'name':lesson.name,
            'cost':'${:.2f}'.format(int(lesson.price/100))
        }
        # save the cart back to sessions
        request.session['lesson_shopping_cart'] = cart
        
        messages.success(request,f"{lesson.name} has been added to your cart!")
        return redirect(reverse('show_lesson_details_route',args=(lesson_id,)))
    else:
        messages.error(request,f"{lesson.name} has already been added to your cart!")
        return redirect(reverse('show_lesson_details_route',args=(lesson_id,)))

def add_product_to_cart(request,product_id):
    cart = request.session.get('product_shopping_cart',{})
    product = get_object_or_404(Product,pk=product_id)
    #Check if product is in cart
    if product_id not in cart:
        cart[product_id]={
            'id':product_id,
            'name':product.name,
            'cost':'${:.2f}'.format(int(product.price/100)),
            'qty': 1,
        }

        #save the cart back to sessions
        request.session['product_shopping_cart'] = cart
        messages.success(request,f"{product.name} has been added to your cart")
        return redirect(reverse('show_product_detail_route',kwargs={'product_id':product_id}))
    else:
        cart[product_id]['qty'] +=1
        request.session['shopping_cart']=cart
        return redirect(reverse('show_product_detail_route',kwargs={'product_id':product_id}))

def view_cart(request):
    #Retrieve the cart
    lesson_cart = request.session.get('lesson_shopping_cart',{})
    product_cart = request.session.get('product_shopping_cart',{})
    total = 0
    for key, item in lesson_cart.items():
        cost_lesson_string = float(item['cost'].strip('$'))
        total += float(cost_lesson_string)
    
    for key, item in product_cart.items():
        cost_product_string = float(item['cost'].strip('$'))
        total += float(cost_product_string * int(item['qty']))

    return render(request,'cart/view_cart.template.html',{
        'lesson_shopping_cart':lesson_cart,
        'product_shopping_cart':product_cart,
        'total':f"{total:.2f}"
    })

def remove_lesson_from_cart(request,lesson_id):
    # retrieve the cart from the session
    cart = request.session.get('lesson_shopping_cart',{})

    # check if lesson in the cart and remove it
    if lesson_id in cart:
        del cart[lesson_id]
        # save back to the session
        request.session['lesson_shopping_cart'] = cart
        messages.success(request,"Lesson has been removed from the cart successfully!")
        return redirect(reverse('show_lesson_details_route',args=(lesson_id,)))

def remove_product_from_cart(request,product_id):
    # retrieve the cart from the session
    cart = request.session.get('product_shopping_cart',{})

    #check if product is in cart and remove it
    if product_id in cart:
        del cart[product_id]
        #save back to the session
        request.session['product_shopping_cart'] = cart
        messages.success(request,"Product has been removed from the cart successfully!")
        return redirect(reverse('show_product_detail_route',kwargs={'product_id':product_id}))
        

def update_quantity_for_product(request,product_id):
    cart = request.session.get('product_shopping_cart')
    if product_id in cart:
        cart[product_id]['qty'] = request.POST['qty']
        request.session['product_shopping_cart'] = cart
        messages.success(request,f"Quantity for {cart[product_id]['name']} has been changed")
    return redirect(reverse('view_cart_route'))

