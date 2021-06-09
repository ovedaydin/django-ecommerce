from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from store.utils import cartData


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    return Response(content)
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def apiOverview(request):
	api_urls = {
		'Order': '/order/<int:num>',
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orderList(request,complete):
	if complete == "all":
		orders = Order.objects.all().order_by('-id')
	if complete == "true":
		orders = Order.objects.filter(complete=True).order_by('-id')
	if complete == "false":
		orders = Order.objects.filter(complete=False).order_by('-id')
	serializer = OrderSerializer(orders, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def order(request,id):
	orders = Order.objects.get(id=id)
	serializer = OrderSerializer(orders)
	return Response(serializer.data)

@api_view(['GET'])
def invoiceList(request,complete):
	if complete == "all":
		invoices = Invoice.objects.all().order_by('-id')
	if complete == "true":
		invoices = Invoice.objects.filter(order__complete=True).order_by('-id')
	if complete == "false":
		invoices = Invoice.objects.filter(order__complete=False).order_by('-id')

	serializer = InvoiceSerializer(invoices, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def cartItems(request):
	data = cartData(request)
	try:
		cartItems = data['cartItems']
	except:
		cartItems =''


	return Response(cartItems)


@api_view(['GET'])
def customerList(request):
	customers = Customer.objects.all().order_by('-id')
	serializer = CustomerSerializer(customers, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def tagList(request):
	tags = Tag.objects.all()
	serializer = TagSerializer(tags, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def productList(request):
	products = Product.objects.all()
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def wholesaleProductList(request):
	products = WholesaleProduct.objects.all()
	serializer = WholesaleProductSerializer(products, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def wholesaleOrderList(request):
	retailer = request.user.wholesalecustomer.retailer
	order, created = WholesaleOrder.objects.get_or_create(retailer=retailer, complete=False)
	serializer = WholesaleOrderSerializer(order, many=False)
	return Response(serializer.data)

@api_view(['GET'])
def wholesaleOrderItemList(request):
	retailer = request.user.wholesalecustomer.retailer
	order, created = WholesaleOrder.objects.get_or_create(retailer=retailer, complete=False)
	orderitems = WholesaleOrderItem.objects.filter(order=order)
	serializer = WholesaleOrderItemSerializer(orderitems, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def updateWholesaleOrder(request):
	retailer = request.user.wholesalecustomer.retailer
	order, created = WholesaleOrder.objects.get_or_create(retailer=retailer, complete=False)
	product = Product.objects.get(name=request.data['name'])
	wholesaleproduct = WholesaleProduct.objects.get(product=product)
	orderitem = WholesaleOrderItem.objects.get_or_create(order=order,wholesaleproduct=wholesaleproduct)
	quantity = orderitem[0].quantity + int(request.data['quantity'])
	serializer = WholesaleOrderItemSerializer(instance=orderitem[0], data={'quantity':quantity}, partial=True)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	task = Task.objects.get(id=pk)
	serializer = TaskSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')
