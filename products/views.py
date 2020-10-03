from django.shortcuts import render,redirect,reverse,get_object_or_404,HttpResponse
from .forms import CategoryForm, ProductForm,SearchForm
from .models import Product, Category
from reviews.models import Product_Review
from django.contrib import messages
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def show_all_products(request):
    all_products = Product.objects.all()
    #Check for queries submitted
    if request.GET:
        queries = ~Q(pk__in=[])

        #if a name is specified, add it to the query
        if 'name' in request.GET and request.GET['name']:
            name = request.GET['name']
            queries = queries & Q(name__icontains=name)

        #if a category is specified, add it to the query
        if 'category' in request.GET and request.GET['category']:
            category = request.GET['category']
            queries= queries & Q(category__in=category)

        if 'price' in request.GET and request.GET['price']:
            selected = request.GET['price']
            if selected == 'Ascending':
                all_products = all_products.filter(queries).order_by('price')
            else:
                all_products = all_products.filter(queries).order_by('-price')


        #update the existing product found
        all_products= all_products.filter(queries)


    search_form = SearchForm(request.GET)
    return render(request,'products/show_all_products.template.html',{
        'products':all_products,
        'search_form':search_form
    })

@staff_member_required
def products_inventory(request):
    if request.method =="POST":
        category_form = CategoryForm(request.POST)
        # Validate form fields
        if category_form.is_valid():
            category_form.save()
            messages.success(request,f"New Category {category_form.cleaned_data['name']} has been created")
            return redirect(reverse(products_inventory))
        else:
            return redirect(reverse(products_inventory))
    else:
        category = Category.objects.all()
        products = Product.objects.all()
        category_form = CategoryForm()
        return render(request,'products/products_inventory.template.html',{
            'form': category_form,
            'products':products,
            'categories': category
        })

@staff_member_required
def delete_category(request,category_id):
    category_to_delete = get_object_or_404(Category,pk=category_id)
    category_to_delete.delete()
    messages.success(request,f"Category {category_to_delete.name} has been deleted")
    return redirect(products_inventory)

@staff_member_required
def create_product(request):
    if request.method =='POST':
        product_form = ProductForm(request.POST)
        # Validate form fields
        if product_form.is_valid():
            product_form.save()
            messages.success(request,f"New Product {product_form.cleaned_data['name']} has been created")
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

@staff_member_required
def update_product(request,product_id):
    product_to_update = get_object_or_404(Product,pk=product_id)

    if request.method == "POST":
        product_form = ProductForm(request.POST, instance=product_to_update)
        # Validate form fields
        if product_form.is_valid():
            product_form.save()
            messages.success(request,f"Product {product_form.cleaned_data['name']} has been updated")
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

@staff_member_required
def delete_product(request,product_id):
    product_to_delete = get_object_or_404(Product,pk=product_id)
    if request.method =="POST":
        product_to_delete.delete()
        messages.success(request,f"Product {product_to_delete.name} has been deleted")
        return redirect(products_inventory)
    else:
        return render(request,'products/delete_product.template.html',{
            'product':product_to_delete
        })


def show_product_detail(request, product_id):
    product_being_viewed = get_object_or_404(Product,pk=product_id)
    reviews = Product_Review.objects.filter(product_bought=product_id)

    return render(request,'products/show_product_detail.template.html',{
        'product': product_being_viewed,
        'reviews': reviews,
    })