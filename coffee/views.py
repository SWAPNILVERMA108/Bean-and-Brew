from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CoffeeOrderForm, CoffeeVarietyForm
from .models import CoffeeOrder, CoffeeVariety, Store

# Create your views here.

def coffee(request):
    coffees = CoffeeVariety.objects.all()
    return render(request,'coffee/coffee.html',{'coffees':coffees})

def coffee_detail(request,coffee_id):
    coffee=get_object_or_404(CoffeeVariety,pk=coffee_id)
    return render(request,'coffee/coffee_detail.html',{'coffee':coffee})


def coffee_stores_view(request):
    stores = None
    searched = False
    if request.method=='POST':
        form = CoffeeVarietyForm(request.POST)
        if form.is_valid():
            coffee_variety = form.cleaned_data['coffee_variety']
            stores = Store.objects.filter(coffee_varieties=coffee_variety)
            searched = True

    else:
        form = CoffeeVarietyForm()
        

    
    return render(request, 'coffee/coffee_stores.html', {'stores': stores, 'form': form, 'searched': searched})


@login_required
def order_create(request):
    initial = {}
    coffee_id = request.GET.get('coffee')
    if coffee_id and CoffeeVariety.objects.filter(pk=coffee_id).exists():
        initial['coffee_variety'] = coffee_id

    if request.method == 'POST':
        form = CoffeeOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            messages.success(request, f'Your order request #{order.pk} was sent to {order.store.name}.')
            return redirect('my_orders')
    else:
        form = CoffeeOrderForm(initial=initial)
    return render(request, 'coffee/order_form.html', {'form': form})


@login_required
def my_orders(request):
    orders = CoffeeOrder.objects.filter(user=request.user).select_related('coffee_variety', 'store')
    return render(request, 'coffee/my_orders.html', {'orders': orders})


@login_required
def store_orders(request):
    if not request.user.is_staff:
        raise PermissionDenied
    orders = CoffeeOrder.objects.select_related('coffee_variety', 'store', 'user')
    if not request.user.is_superuser:
        orders = orders.filter(store__staff_members=request.user)
    return render(request, 'coffee/store_orders.html', {'orders': orders})
