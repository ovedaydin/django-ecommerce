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


def wholesalePayment(request):
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

    user = request.user
    customer = user.wholesalecustomer
    data = wholesaleCartData(request)
    payment, created = WholesalePayment.objects.get_or_create(order=data['order'])
    print(data)
    order = data['order']
    cartItems= data['cartItems']
    items = data['items']
    print(order.get_cart_total)

    request = dict([('locale', 'tr')])
    request['conversationId'] = str(payment.conversationId)
    request['price'] = str(order.get_cart_total)
    # Create a calculator for wholesale payments, commission can change, create a object for commission
    commission = Commission.objects.get(id=1)
    request['paidPrice'] = "{:.2f}".format(100*(order.get_cart_total/(100 - commission.rate))+commission.fixed)
    print(request['paidPrice'])
    request['basketId'] = 'W' + str(order.id)

    request['paymentGroup'] = 'PRODUCT'

    request['callbackUrl'] = 'http://localhost:8000/payment/check/wholesale/'+str(payment.id)

    buyer = dict([('id', str(customer.id))])
    buyer['name'] = str(customer.name)
    buyer['surname'] = str(customer.name)
    buyer['gsmNumber'] = '+905350000000'
    buyer['email'] = 'email@email.com'
    buyer['identityNumber'] = '74300864791'
    buyer['lastLoginDate'] = '2015-10-05 12:43:35'
    buyer['registrationDate'] = '2013-04-21 15:12:09'
    buyer['registrationAddress'] = 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1'
    buyer['ip'] = '85.34.78.112'
    buyer['city'] = 'Istanbul'
    buyer['country'] = 'Turkey'
    buyer['zipCode'] = '34732'
    request['buyer'] = buyer

    address = dict([('address', 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1')])
    address['zipCode'] = '34732'
    address['contactName'] = 'Jane Doe'
    address['city'] = 'Istanbul'
    address['country'] = 'Turkey'
    request['shippingAddress'] = address
    request['billingAddress'] = address

    basket_items = []
    for item in items:
        for x in range(0, item.quantity):
            basket_item = dict([('id', str(item.wholesaleproduct.id))])
            basket_item['name'] = item.wholesaleproduct.product.name
            basket_item['category1'] = 'Collectibles'
            basket_item['category2'] = 'Accessories'
            basket_item['itemType'] = 'PHYSICAL'
            basket_item['price'] = str(item.wholesaleproduct.price)
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
