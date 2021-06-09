from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    uuid = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        if self.name:
            return str(self.name)
        return str(self.uuid)
# tag is used for categories
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2,blank= True )
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)
    descripton = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, blank=True, null=True)
    is_bundle = models.BooleanField(default=False, null=True, blank=False)
    has_variant = models.BooleanField(default=False, null=True, blank=False)
    on_sale = models.BooleanField(default=True, null=True, blank=False)
    def __str__(self):
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str (str(self.product) + ' ' +  str(self.name))

class ListProduct(models.Model):
    main_product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='main_product_set')
    included_product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='included_product_set')
    index = models.IntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return str (str(self.main_product) +':'+ str(self.index)+ ' has ' +  str(self.included_product))

class BundleVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str (str(self.product) + ' ' +  str(self.name))

class BundleVariantProduct(models.Model):
    bundle_variant = models.ForeignKey(BundleVariant, on_delete=models.CASCADE,  related_name='bundle_variant_set')
    included_product = models.ForeignKey(Product, on_delete=models.CASCADE,  related_name='included_variant_product_set')
    index = models.IntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return str (str(self.bundle_variant) +':'+ str(self.index)+ ' has ' +  str(self.included_product))


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    uuid = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=200, default="", null=False, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    takeaway = models.BooleanField(default=False, null=True, blank=False)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)
    date_expected = models.DateField(null=True, blank=True)
    shipping_cost = models.DecimalField(default=0.00,max_digits=7, decimal_places=2)
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems]) + self.shipping_cost
        return total

    @property
    def get_cart_total_no_shipping(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_tax(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        total += self.shipping_cost
        tax = (total/100)*8
        return round(tax,2)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    uuid = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='shipping',on_delete=models.SET_NULL, blank=True, null=True)

    contact = models.CharField(max_length=200, null=False, blank=False)

    name = models.CharField(max_length=200, null=False, blank=False)
    surname = models.CharField(max_length=200, null=False, blank=False)

    company = models.CharField(max_length=200, default="", null=False, blank=True)
    address1 = models.CharField(max_length=200,default="empty", null=False, blank=False)
    address2 = models.CharField(max_length=200,default=" ", null=True, blank=False)
    district = models.CharField(max_length=200, null=False, blank=False)

    city = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=200, null=False, blank=False)

    postcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    use_for_invoice = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        a = str(self.address1) + " "
        if self.address2:
            a += str(self.address2) + " "
        a += str(self.district) + " "
        a += str(self.city) + " "
        a += str(self.postcode) + " "
        return str(a)

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    uuid = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='invoice',on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=200, null=False, blank=False)
    surname = models.CharField(max_length=200, null=False, blank=False)

    company = models.CharField(max_length=200, default="", null=False, blank=True)
    address1 = models.CharField(max_length=200,default="empty", null=False, blank=False)
    address2 = models.CharField(max_length=200,default=" ", null=True, blank=False)

    city = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=200, null=False, blank=False)

    postcode = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        a = str(self.address1) + " "
        if self.address2:
            a += str(self.address2) + " "
        a += str(self.city) + " "
        a += str(self.postcode) + " "
        return str(a)

    @property
    def get_fullname(self):
        fullname = self.name + " " + self.surname
        return fullname



class Subscribe(models.Model):
    contact = models.CharField(max_length=200, null=True)
    uuid = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.contact
