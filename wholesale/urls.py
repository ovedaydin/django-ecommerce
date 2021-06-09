from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.wholesale, name= 'wholesale'),
    path('order', views.wholesaleOrder, name= 'wholesaleOrder'),
    path('user/', views.wholesaleUser, name= 'wholesaleUser'),
    path('checkout/', views.wholesaleCheckout, name= 'wholesaleCheckout'),
    path('user/update_user/', views.wholesaleUpdateUser),
    path('payment/', views.payment, name= 'wholesalePayment'),






    ]
