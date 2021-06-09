from django.db import models
from store.models import *
from wholesale.models import *

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    conversationId = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    token = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.order)

class WholesalePayment(models.Model):
    order = models.ForeignKey(WholesaleOrder, on_delete=models.SET_NULL, blank=True, null=True)
    conversationId = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    token = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.order)

class PaymentKey(models.Model):
    api_key = models.CharField(max_length=200, null=True, blank=True)
    secret_key = models.CharField(max_length=200, null=True, blank=True)
    base_url = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(self.id)

class Commission(models.Model):
    rate = models.DecimalField(max_digits=2, decimal_places=0)
    fixed = models.DecimalField(max_digits=2, decimal_places=2)
    def __str__(self):
        return str(self.id)
