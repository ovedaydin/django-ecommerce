from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('auth/', obtain_auth_token, name="obtain_auth_token"),

    path('customers/', views.customerList),
    path('tags/', views.tagList),
    path('products/', views.productList),
    path('orders/<str:complete>', views.orderList),
    path('order/<int:id>', views.order),
    path('invoices/<str:complete>', views.invoiceList),
    path('wholesale/products/', views.wholesaleProductList),
    path('wholesale/orders/', views.wholesaleOrderList),
    path('wholesale/orderitems/', views.wholesaleOrderItemList),
    path('wholesale/updateorder/', views.updateWholesaleOrder),

    path('cartItems/', views.cartItems),
    ]
