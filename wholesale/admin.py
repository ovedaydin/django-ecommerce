from django.contrib import admin
from .models import *

admin.site.register(Chain)
admin.site.register(Retailer)
admin.site.register(WholesaleCustomer)
admin.site.register(WholesaleProduct)
admin.site.register(WholesaleSpeacialPricedProduct)
admin.site.register(WholesaleOrder)
admin.site.register(WholesaleOrderItem)
admin.site.register(WholesaleShippingAddress)
# Register your models here.
