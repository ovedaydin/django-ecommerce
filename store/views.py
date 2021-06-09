import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
import datetime
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import *
from .utils import cartData, cookieCart, guestOrder, getUUID
from .forms import CreateUserForm
from .decorators import *
from .payment import retailPayment
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@allowed_users(allowed_roles=['admin'])
def admin(request):
    return render(request, 'admin/main.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password = password)

        if user is not None:
            login(request, user)
            if request.user.groups.all()[0].name == 'wholesale':
                return redirect('wholesale')
            #return redirect('store')
            return redirect('http://127.0.0.1:3000/')
        else:
            messages.info(request, 'Username Or Password is incorrect')

    return render(request, 'user/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            customer = Customer.objects.get(email=user.email)
            if customer:
                customer.user = user
                customer.save()
            Customer.objects.get_or_create(user=user, email=user.email)
            messages.success(request,'Hesap oluşturuldu ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'user/register.html', context)


#Retail

@allowed_users(allowed_roles=['admin', 'customer'])
def userPage(request):
    data = cartData(request)
    cartItems = data['cartItems']

    customer = Customer.objects.get(user=request.user)
    orders = []
    for order in Order.objects.filter(customer=customer, complete=True):
        orders.append(order)
    orders.reverse()
    context = {'cartItems':cartItems, 'orders': orders}
    return render(request, 'store/user.html', context)

@allowed_users(allowed_roles=['admin', 'customer'])
def orderPage(request,orderId):
    data = cartData(request)
    order = Order.objects.get(id=orderId)
    items = order.orderitem_set.all()
    cartItems = data['cartItems']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    if request.user != order.customer.user:
        return redirect('user')
    return render(request, 'store/order.html', context)


def product(request, productId):
    product = Product.objects.get(id=productId)
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems':cartItems, "product":product}

    if product.is_bundle and product.has_variant:
        bundle_variants = BundleVariant.objects.all().filter(product=product)
        print(bundle_variants)
        bundle_variant_dict = {}
        for bundle_variant in bundle_variants:
            bundle = BundleVariantProduct.objects.all().filter(bundle_variant=bundle_variant)
            print(bundle)
            bundle_products = {}
            for bundle_product in bundle:
                bundle_products[bundle_product.index] = []

            for x in bundle_products:
                list = []
                for bundle_product in bundle:
                    if bundle_product.index == x:
                        list.append(bundle_product.included_product)
                bundle_products[x] = list
            bundle_variant_dict[bundle_variant] = bundle_products
        print(bundle_variant_dict)
        context['bundle_variant'] = bundle_variant_dict
    elif product.is_bundle:
        bundle = ListProduct.objects.all().filter(main_product=product)
        bundle_products = {}
        for bundle_product in bundle:
            bundle_products[bundle_product.index] = bundle_product.included_product

        #for x in bundle_products:
        #    list = []
        #    for bundle_product in bundle:
        #        if bundle_product.index == x:
        #            list.append(bundle_product.included_product)
        #    bundle_products[x] = list
        print(bundle_products)
        context['bundle'] = bundle_products
    elif product.has_variant:
        variants = ProductVariant.objects.all().filter(product=product)
        context['variants'] = variants
        print(variants)



    return render(request, 'store/product-designed.html',context)

def tag(request, tag):
    data = cartData(request)
    cartItems = data['cartItems']
    if tag == 'all':
        products = Product.objects.all()
        context = {'products':products, 'cartItems':cartItems, 'tag':'Ürünler'}
    else:
        products = Product.objects.filter(tags__name=tag)
        context = {'products':products, 'cartItems':cartItems, 'tag':tag}
    return render(request, 'store/tag-collection.html',context)


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    orderItems = OrderItem.objects.all()
    products = Product.objects.all()

    if OrderItem.objects.all():
        collection = {}
        for orderItem in OrderItem.objects.all():
            product = orderItem.product
            try:
                checker = collection[product]
            except:
                checker = 0
            if checker >= 1:
                collection[product] +=  orderItem.quantity
            else:
                collection[product] =  orderItem.quantity

        print(collection)
        collectionByTags = {}
        for item in collection:
            tag = item.tags
            try:
                currentProduct = collectionByTags[tag]
            except:
                currentProduct = item

            if collection[item] >= collection[currentProduct]:
                collectionByTags[tag] = item
            print(collectionByTags[tag])

        collectionProducts = []
        for item in collectionByTags:
            collectionProducts.append(collectionByTags[item])
        print(collectionProducts)

        populars = []

        for i in range(0, 3):
            max1 = 0

            for j in collection:
                if collection[j] > max1:
                    max1 = collection[j]
                    removedJ = j


            collection[removedJ] = 0
            populars.append(removedJ)

        print(populars)
    else:
        collectionProducts = []
        populars = []
        for tag in Tag.objects.all():
            if Product.objects.all().filter(tags=tag):
                for product in Product.objects.all().filter(tags=tag):
                    addProduct = product
                collectionProducts.append(addProduct)

        for i in range(0, 3):
            populars.append(collectionProducts[i])

    print(collectionProducts)

    context = {'products':products, 'cartItems':cartItems, 'collectionProducts': collectionProducts, 'populars':populars}
    #return render(request,'store/store.html',context)
    return render(request,'store/store-designed.html',context)

def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items':items, 'order':order,'cartItems':cartItems}
    print(context['order'])
    return render(request,'store/cart-redesigned.html',context)

def checkout(request):
    if request.method == 'POST':
        subscribe = request.POST.get('subscribe')
        contact=request.POST.get('contact-info')
        uuid = getUUID(request)
        try:
            order = Order.objects.get(uuid=uuid,complete=False)
        except:
            order = Order.objects.get(customer=request.user.customer,complete=False)
        if subscribe and contact:
            subscribe, created = Subscribe.objects.get_or_create(contact=contact, uuid=uuid)
        order.contact = contact
        if request.POST.get("ship") == "takeaway":
            order.takeaway = True
            order.save()
            try:
                address = ShippingAddress.objects.get(order = order)
                address.delete()
            except:
                pass

        if request.POST.get("ship") == "shipping":
            order.takeaway = False
            order.save()
            address, created = ShippingAddress.objects.get_or_create(order = order)
            try:
                address.customer = request.user.customer
            except:
                pass
            address.uuid = uuid
            address.order = order
            address.contact = contact

            address.name = request.POST.get("name")
            address.surname = request.POST.get("surname")

            address.address1 = request.POST.get("address1")
            address.address2 = request.POST.get("address2")
            address.district = request.POST.get("district")
            address.city = request.POST.get("city")
            address.phone = request.POST.get("phone")
            address.postcode = request.POST.get("postcode")
            if request.POST.get("saveShipping"):
                address.use_for_invoice = True
            else:
                address.use_for_invoice = False
            address.save()
        return redirect('checkoutDate')

    data = cartData(request)
    items = data['items']
    order = data['order']
    order.shipping_cost = 0
    order.save()
    try:
        address = ShippingAddress.objects.get(order=order)
    except:
        address = ""

    shipping_text  = "Bir sonraki adımda hesaplanır"
    context = {'items':items, 'order':order,'address':address,"shipping_text":shipping_text }
    return render(request,'checkout/checkout-info.html', context)




    return render(request,'store/checkout.html',context)

def checkoutDate(request):


    try:
        uuid = getUUID(request)
        order = Order.objects.get(uuid=uuid,complete=False)
    except:
        order = Order.objects.get(customer=request.user.customer,complete=False)


    if request.method == 'POST':
        print(request.POST)
        order.date_expected = request.POST.get("date")
        order.shipping_cost = request.POST.get("shipping_cost")
        order.save()
        return redirect('checkoutPayment')

    order.shipping_cost = 0
    order.save()

    if order.takeaway:
        address = "Ali Ferruh Sk. No:13 Hasanpaşa, 34722 Kadıköy/İstanbul"
        contact = order.contact
        shippingCost = 0
        shippingCostDiscount = 0
        shipping = {
        "shippingCost": shippingCost,
        "shippingCostDiscount": shippingCostDiscount,
        "withShipping": order.get_cart_total - order.shipping_cost+ shippingCost,
        "withShippingDiscount": order.get_cart_total - order.shipping_cost+shippingCostDiscount,
        }
    else:
        address = ShippingAddress.objects.get(order=order)
        contact = address.contact
        shippingCost = 20
        shippingCostDiscount = 10
        shipping = {
        "shippingCost": shippingCost,
        "shippingCostDiscount": shippingCostDiscount,
        "withShipping": order.get_cart_total+ shippingCost,
        "withShippingDiscount": order.get_cart_total+shippingCostDiscount,
        }


    data = cartData(request)
    items = data['items']
    order = data['order']
    shipping_text = "Bu adımda hesaplanır"
    context = {"address":address, "shipping":shipping,"contact":contact,'items':items, 'order':order,'shipping_text':shipping_text }
    return render(request,'checkout/checkout-date.html',context)

def checkoutPayment(request):
    try:
        uuid = getUUID(request)
        order = Order.objects.get(uuid=uuid,complete=False)
    except:
        order = Order.objects.get(customer=request.user.customer,complete=False)

    if order.takeaway:
        address = "Ali Ferruh Sk. No:13 Hasanpaşa, 34722 Kadıköy/İstanbul"
        contact = order.contact
    else:
        address = ShippingAddress.objects.get(order=order)
        contact = address.contact

    try:
        invoice = Invoice.objects.get(order=order)
    except:
        invoice = ""

    if invoice == "" and not order.takeaway:
        try:
            invoice_ = ShippingAddress.objects.get(order=order)
            if invoice_.use_for_invoice:
                invoice = invoice_
        except:
            pass

    data = cartData(request)
    items = data['items']
    order = data['order']
    shipping_text = str(order.shipping_cost) + " TL"
    print(order.id)
    context = {"address":address, "contact":contact,'items':items, 'order':order, 'invoice':invoice,"shipping_text":shipping_text}

    if request.method == 'POST':
        payment_type = request.POST.get("payment")

        invoice, created = Invoice.objects.get_or_create(order = order)
        try:
            invoce.customer = request.user.customer
        except:
            pass
        invoice.uuid = uuid
        invoice.order = order

        invoice.name = request.POST.get("name")
        invoice.surname = request.POST.get("surname")

        invoice.address1 = request.POST.get("address1")
        invoice.address2 = request.POST.get("address2")
        invoice.city = request.POST.get("city")
        invoice.phone = request.POST.get("phone")
        invoice.postcode = request.POST.get("postcode")
        invoice.save()

        if payment_type == "online_payment":
            content = retailPayment(request)
            context= {"checkoutFormContent":content['checkoutFormContent'] ,"address":address, "contact":contact,'items':items, 'order':order,'invoice':invoice}
            return render(request, 'checkout/iyzico.html', context)
    return render(request,'checkout/checkout-payment.html',context)

def checkoutCheck(request,result):
    try:
        uuid = getUUID(request)
        order = Order.objects.get(uuid=uuid,complete=False)
    except:
        order = Order.objects.get(customer=request.user.customer,complete=False)
    if result == 'success':
        order.complete = True
        order.save()

    context = {"result": result}
    return render(request,'checkout/checkout-check.html',context)



@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId:', productId)
    print('Action:', action)
    if request.user.is_anonymous:
        order, created = Order.objects.get_or_create(uuid=getUUID(request),complete=False)
    else:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    product = Product.objects.get(id=productId)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request,data)


    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
        order.status = 'Pending'
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer = customer,
        order = order,
        address = data['shipping']['address'],
        city = data['shipping']['city'],
        state = data['shipping']['state'],
        zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete!', safe=False)
