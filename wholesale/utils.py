import json
from .models import *


def wholesaleCartData(request):
    wholesaleCustomer = request.user.wholesalecustomer
    order, created = WholesaleOrder.objects.get_or_create(retailer=wholesaleCustomer.retailer,complete=False, status="Pending")
    items = order.wholesaleorderitem_set.all()
    cartItems = order.get_cart_items
    print(order.get_cart_total)
    return {'cartItems':cartItems, 'order': order,'items':items}
