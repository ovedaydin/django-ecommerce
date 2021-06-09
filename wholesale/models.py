from django.db import models
from store.models import *
#Chain contains Retailer.
class Chain(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Retailer(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    chain = models.ForeignKey(Chain, on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return str(self.name)
#if customer is admin of the chain, do not need a retailer field.
#admin-chain can be put in user groups ?????


class WholesaleCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL ,null=True, blank=True)
    chain = models.OneToOneField(Chain, on_delete=models.SET_NULL ,null=True, blank=True)
    chainAdmin = models.BooleanField(default=False, null=True, blank=False)
    retailer = models.ForeignKey(Retailer,on_delete=models.SET_NULL ,null=True, blank=True )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

class WholesaleProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.SET_NULL ,null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return str(self.product.name)

#Some customers get a speacial price for some products.
class WholesaleSpeacialPricedProduct(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    product = models.OneToOneField(WholesaleProduct, on_delete=models.SET_NULL ,null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    def __str__(self):
        return str(self.product.product.name)

class WholesaleOrder(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.wholesaleorderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.wholesaleorderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class WholesaleOrderItem(models.Model):
    wholesaleproduct = models.ForeignKey(WholesaleProduct, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(WholesaleOrder, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.wholesaleproduct.price
        return total

class WholesaleShippingAddress(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address
