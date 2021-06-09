from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin/',views.admin, name='admin'),
    path('login/',views.loginPage, name='login'),
    path('register/',views.register, name='register'),
    path('logout/',views.logoutUser, name='logout'),
    path('user/', views.userPage, name= 'user'),
    path('order/<str:orderId>', views.orderPage, name='orderPage'),

    path('',views.store, name='store'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('checkout/date',views.checkoutDate, name='checkoutDate'),
    path('checkout/payment',views.checkoutPayment, name='checkoutPayment'),
    path('checkout/check/<str:result>', views.checkoutCheck, name='checkoutCheck'),

    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/',views.processOrder, name='process_order'),
    path('products/<str:productId>',views.product,name='products'),
    path('tag/<str:tag>/',views.tag,name='tag'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ]
