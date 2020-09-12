from django.shortcuts import render,redirect,reverse,get_object_or_404,HttpResponse
from .forms import CategoryForm, ProductForm
from .models import Product, Category

# Create your views here.

def show_all_products(request):
    return render(request,'products/show_all_products.template.html')

def show_product_detail(request, product_id):
    product_being_viewed = get_object_or_404(Product,pk=product_id)
    return render(request,'products/show_product_detail.template.html',{
        'product':product_being_viewed
    })

def products_inventory(request):
    if request.method =="POST":
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect(products_inventory)
        else:
            return redirect(products_inventory)
    else:
        category = Category.objects.all()
        products = Product.objects.all()
        category_form = CategoryForm()
        return render(request,'products/products_inventory.template.html',{
            'form': category_form,
            'products':products,
            'categories': category
        })

def delete_category(request,category_id):
    category_to_delete = get_object_or_404(Category,pk=category_id)
    category_to_delete.delete()
    return redirect(products_inventory)

def create_product(request):
    if request.method =='POST':
        product_form = ProductForm(request.POST)
        # Validate form fields
        if product_form.is_valid():
            product_form.save()
            return redirect(products_inventory)
        else:
            return render(request,'products/create_product.template.html',{
                'form':product_form
            })
    else:
        product_form = ProductForm()
        return render(request,'products/create_product.template.html',
        {
            'form':product_form
        })

def update_product(request,product_id):
    product_to_update = get_object_or_404(Product,pk=product_id)

    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product_to_update)

        if product_form.is_valid():
            product_form.save()
            return redirect(products_inventory)
        else:
            return render(request, 'products/update_product.template.html',{
                "form": product_form
            })

    else:
        product_form = ProductForm(instance=product_to_update)
        return render(request,'products/update_product.template.html',{
            'form':product_form
        })

def delete_product(request,product_id):
    product_to_delete = get_object_or_404(Product,pk=product_id)
    if request.method =="POST":
        product_to_delete.delete()
        return redirect(products_inventory)
    else:
        return render(request,'products/delete_product.template.html',{
            'product':product_to_delete
        })