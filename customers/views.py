from django.shortcuts import render,redirect,get_object_or_404
from .models import Customer
from .forms import CustomerProfileForm


# Create your views here.
def show_user_profile(request):
    user_profile=get_object_or_404(Customer,pk=request.user)
    return render(request,'customers/show_profile.template.html',{
    'profile': user_profile
    })

def update_profile(request,user_id):
    user_to_update = get_object_or_404(Customer,pk=user_id)

    if request.method == "POST":
        customer_form = CustomerProfileForm(request.POST, instance=user_to_update)

        if customer_form.is_valid():
            customer_form.save()
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

