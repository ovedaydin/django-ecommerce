from django.urls import path
from .views import *

urlpatterns = [

    path('check/<str:paymentId>', check, name='check'),
    

]
