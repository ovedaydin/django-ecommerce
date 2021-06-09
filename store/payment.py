import json
from payment.models import *
from wholesale.utils import *
from store.utils import *
import iyzipay

options = {
    'api_key': 'api_key',
    'secret_key': 'secret_key',
    'base_url': 'base_url'
}


def retailPayment(request):
    try:
        paymentkey, created = PaymentKey.objects.get_or_create(id=1)
    except PaymentKey.DoesNotExist:
        paymentkey = None

    if paymentkey:
        api_key = paymentkey.api_key
        secret_key = paymentkey.secret_key
        base_url = paymentkey.base_url

        options = {
            'api_key': api_key,
            'secret_key': secret_key,
            'base_url': base_url
        }

    #user = request.user
    #customer = user.customer
    data = cartData(request)
    payment, created = Payment.objects.get_or_create(order=data['order'])
    order = data['order']
    cartItems= data['cartItems']
    items = data['items']
    invoice = Invoice.objects.get(order=order)

    request = dict([('locale', 'tr')])
    request['conversationId'] = str(payment.conversationId)
    request['price'] = str(order.get_cart_total)
    request['paidPrice'] = str(order.get_cart_total)
    request['basketId'] = 'R' + str(order.id)
    request['paymentGroup'] = 'PRODUCT'
    request['callbackUrl'] = 'http://localhost:8000/payment/check/'+str(payment.id)

    buyer = dict([('id', str(invoice.uuid))])
    buyer['name'] = str(invoice.name)
    buyer['surname'] = str(invoice.surname)
    buyer['gsmNumber'] = str(invoice.phone)
    buyer['email'] = 'email@email.com'
    buyer['identityNumber'] = '11111111111'
    buyer['lastLoginDate'] = '2015-10-05 12:43:35'
    buyer['registrationDate'] = '2013-04-21 15:12:09'
    buyer['registrationAddress'] = str(invoice.address1)
    buyer['ip'] = '85.34.78.112'
    buyer['city'] = 'Istanbul'
    buyer['country'] = 'Turkey'
    buyer['zipCode'] = '34732'
    request['buyer'] = buyer

    address = dict([('address', str(invoice.address1))])
    address['zipCode'] = str(invoice.postcode)
    address['contactName'] = str(invoice.get_fullname)
    address['city'] = str(invoice.city)
    address['country'] = 'Turkey'

    request['shippingAddress'] = address
    request['billingAddress'] = address

    basket_items = []
    for item in items:
        for x in range(0, item.quantity):
            basket_item = dict([('id', str(item.product.id))])
            basket_item['name'] = item.product.name
            basket_item['category1'] = 'Collectibles'
            basket_item['category2'] = 'Accessories'
            basket_item['itemType'] = 'PHYSICAL'
            basket_item['price'] = str(item.product.price)
            basket_items.append(basket_item)

    if order.shipping_cost != 0.00:
        basket_item = dict([('id', "0")])
        basket_item['name'] = "Kargo"
        basket_item['category1'] = 'Collectibles'
        basket_item['category2'] = 'Accessories'
        basket_item['itemType'] = 'PHYSICAL'
        basket_item['price'] = str(order.shipping_cost)
        basket_items.append(basket_item)

    request['basketItems'] = basket_items
    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)


    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(json_content)
    token = json_content['token']
    payment.token = token
    payment.save()
    return json_content
