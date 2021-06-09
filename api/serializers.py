from rest_framework import serializers

from store.models import *
from wholesale.models import *

class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields ='__all__'



class InvoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Invoice
		fields ='__all__'

class ShippingSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShippingAddress
		fields ='__all__'

class OrderSerializer(serializers.ModelSerializer):
	invoice = InvoiceSerializer(many=True)
	shipping = ShippingSerializer(many=True)
	get_cart_total = serializers.ReadOnlyField()
	#shipping  = serializers.StringRelatedField(many=True)
	class Meta:
		model = Order
		fields ="__all__"
		depth = 1



class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields ='__all__'

class ProductSerializer(serializers.ModelSerializer):
	tags = TagSerializer(many=False, read_only=True)
	class Meta:
		model = Product
		fields ='__all__'

class WholesaleProductSerializer(serializers.ModelSerializer):
	product = ProductSerializer(many=False, read_only=True)
	tags = TagSerializer(many=False, read_only=True)
	class Meta:
		model = WholesaleProduct
		fields = '__all__'

class WholesaleOrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = WholesaleOrder
		fields = '__all__'

class WholesaleOrderItemSerializer(serializers.ModelSerializer):
	wholesaleproduct = WholesaleProductSerializer(many=False, read_only=True)
	order = WholesaleOrderSerializer(many=False, read_only=True)
	class Meta:
		model = WholesaleOrderItem
		fields = '__all__'
