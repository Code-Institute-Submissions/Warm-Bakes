from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .forms import CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def show_user_profile(request):
    user_profile=get_object_or_404(Customer,user=request.user)
    return render(request,'customers/show_profile.template.html',{
    'profile': user_profile
    })
@login_required
def update_profile(request):
    user_to_update = get_object_or_404(Customer,user=request.user)

    if request.method == "POST":
        customer_form = CustomerProfileForm(request.POST, instance=user_to_update)

        if customer_form.is_valid():
            customer_form.save()
            messages.success(request,f"Customer profile has been updated")
            return redirect(show_user_profile)
        else:
            return render(request, 'customers/update_profile.template.html',{
                "form": customer_form
            })

    else:
        customer_form = CustomerProfileForm(instance=user_to_update)
        return render(request,'customers/update_profile.template.html',{
            'form':customer_form
        })

