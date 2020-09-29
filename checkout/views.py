from django.shortcuts import render,reverse,get_object_or_404,redirect,HttpResponse
#import settings to get access to public stripe key
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from lessons.models import Lesson
from products.models import Product
from customers.models import Customer
from django.contrib.auth.models import User
from .models import Lesson_Order,Product_Order
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib import messages
import json

from uuid import UUID
# Create your views here.


class UUIDEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,UUID):
            #if the object is uuid, return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self,obj)

@login_required
def checkout(request):
    #Get the secret key from settings.py
    stripe.api_key=settings.STRIPE_SECRET_KEY

    #Retrieve the shopping carts
    lesson_cart = request.session.get('lesson_shopping_cart',{})
    product_cart = request.session.get('product_shopping_cart',{})

    #Create the line items
    lesson_line_items = []
    all_lesson_ids = []

    product_line_items = []
    all_product_ids = []

    # Go through each lesson in the shopping cart
    for key, cart_lesson_item in lesson_cart.items():
        # Retrieve the lesson by its id from the database
        lesson_model = get_object_or_404(Lesson,pk=cart_lesson_item["id"])

        #create line item
        lesson_item = {
            "name": lesson_model.name,
            "amount":int(lesson_model.price),
            "currency": "sgd",
            "quantity": 1,
        }

        lesson_line_items.append(lesson_item)
        all_lesson_ids.append({
            'lesson_id':lesson_model.id,
            'qty':1
        })

    #Go through each product in the shopping cart
    for key, cart_product_item in product_cart.items():
        # Retrieve the product by its id from the database
        product_model = get_object_or_404(Product,pk=cart_product_item['id'])

        #create line item
        product_item = {
            "name": product_model.name,
            "amount": int(product_model.price),
            "quantity":cart_product_item['qty'],
            "currency":"sgd",
        }
        
        product_line_items.append(product_item)
        all_product_ids.append({
            'product_id':product_model.id,
            'qty':cart_product_item['qty']
        })
    
    # Get the current website
    current_site = Site.objects.get_current()

    # Get the domain name
    domain = current_site.domain

    combined_line_items = lesson_line_items + product_line_items
    #Create a payment session to represent the current transaction
    session = stripe.checkout.Session.create(
        payment_method_types=["card"], #accept credit cards
        line_items = combined_line_items,
        client_reference_id=request.user.id,
        metadata={
            "all_lesson_ids": json.dumps(all_lesson_ids),
            "all_product_ids": json.dumps(all_product_ids,cls=UUIDEncoder),
        },
        mode="payment",
        success_url =domain + reverse('checkout_success_route'),
        cancel_url = domain+ reverse('checkout_cancelled_route')
    )
    return render(request,"checkout/checkout.template.html",{
        "session_id":session.id,
        "public_key": settings.STRIPE_PUBLISHABLE_KEY
    })


def checkout_success(request):
    #empty the shopping cart
    request.session['lesson_shopping_cart']={}
    request.session['product_shopping_cart']={}
    messages.success(request,"Checkout Success!")
    return redirect(reverse('homepage'))

def checkout_cancelled(request):
    messages.error(request,"Error in Checkout!")
    return redirect(reverse('homepage'))

@csrf_exempt
def payment_completed(request):
    payload=request.body
    endpoint_secret=settings.STRIPE_ENDPOINT_SECRET
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header,endpoint_secret
        )
    except ValueError as e:
        # invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # invalid signature
        print(e)
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type']=='checkout.session.completed':
        session = event['data']['object']
        #Fufill the purchase...
        handle_payment(session)
    
    return HttpResponse(status=200)



def handle_payment(session):
    customer = get_object_or_404(User,pk=session["client_reference_id"])

    all_lesson_ids = json.loads(session['metadata']['all_lesson_ids'])
    all_product_ids = json.loads(session['metadata']['all_product_ids'])
    for lesson in all_lesson_ids:
        lesson_model = get_object_or_404(Lesson,pk=lesson["lesson_id"])

        #Create the Lesson Orders Model
        lesson_order = Lesson_Order()
        lesson_order.lesson = lesson_model
        lesson_order.customer = customer
        lesson_order.price = lesson_model.price
        lesson_order.save()
    
    for product in all_product_ids:
        product_model = get_object_or_404(Product,pk=product["product_id"])

        #Create the Product Orders Model
        product_order = Product_Order()
        product_order.product = product_model
        product_order.customer = customer
        product_order.price = product_model.price
        product_order.quantity = int(product["qty"])
        product_order.save()

@login_required
def view_my_purchases(request):
    lesson_orders = Lesson_Order.objects.filter(customer=request.user)
    product_orders = Product_Order.objects.filter(customer=request.user)
    return render(request,'checkout/user_purchases.template.html',{
        'product_orders':product_orders,
        'lesson_orders':lesson_orders
    })