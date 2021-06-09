from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Invoice)
admin.site.register(ListProduct)
admin.site.register(BundleVariant)
admin.site.register(BundleVariantProduct)
admin.site.register(Subscribe)

# Register your models here.
