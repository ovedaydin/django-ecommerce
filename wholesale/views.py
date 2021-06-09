import json
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
import datetime
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .models import *
from .utils import wholesaleCartData
from store.decorators import *
from .payment import wholesalePayment


@allowed_users(allowed_roles=['admin','wholesale'])
def wholesale(request):
    data = wholesaleCartData(request)
    cartItems = data['cartItems']
    wholesaleCustomer = WholesaleCustomer.objects.get(user=request.user)
    context = {'customer':wholesaleCustomer,'cartItems':cartItems}
    return render(request,'wholesale/dashboard.html', context)

@allowed_users(allowed_roles=['admin','wholesale'])
def wholesaleUser(request):
    data = wholesaleCartData(request)
    cartItems = data['cartItems']
    wholesaleCustomer = WholesaleCustomer.objects.get(user=request.user)
    context = {'customer':wholesaleCustomer,'cartItems':cartItems}
    return render(request,'wholesale/user.html', context)

@allowed_users(allowed_roles=['admin','wholesale'])
def wholesaleOrder(request):
    wholesaleCustomer = WholesaleCustomer.objects.get(user=request.user)
    products = Product.objects.all()
    tags = Tag.objects.all()
    data = wholesaleCartData(request)
    order = data['order']
    cartItems = data['cartItems']
    context = {'customer':wholesaleCustomer,'cartItems':cartItems,'order':order}
    return render(request,'wholesale/order.html', context)

@allowed_users(allowed_roles=['admin','wholesale'])
def wholesaleCheckout(request):
    wholesaleCustomer = WholesaleCustomer.objects.get(user=request.user)
    data = wholesaleCartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    context = {'customer':wholesaleCustomer,'cartItems':cartItems,'order':order, 'items':items}
    return render(request,'wholesale/checkout.html', context)

def wholesaleUpdateUser(request):
    data = json.loads(request.body)
    print(data)
    user = request.user
    customer = user.wholesalecustomer
    user.username = data['form']['username']
    customer.name = data['form']['name']
    customer.email = data['form']['email']
    customer.phone_number = data['form']['phone_number']

    user.save()
    customer.save()
    return JsonResponse('Payment complete!', safe=False)

def payment(request):
    wholesaleCustomer = WholesaleCustomer.objects.get(user=request.user)
    data = wholesaleCartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    content = wholesalePayment(request)
    context = {"checkoutFormContent": content['checkoutFormContent'],'customer':wholesaleCustomer,'cartItems':cartItems,'order':order, 'items':items}

    return render(request, 'wholesale/payment.html', context)
