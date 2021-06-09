import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from .models import *
from wholesale.utils import *
from store.utils import *
from .utils import *

@require_http_methods(['POST'])
@csrf_exempt
def check(request, paymentId):
    token = request.POST.get('token')
    payment = Payment.objects.get(id=paymentId)
    sonuc = checker(token,payment)
    return redirect('checkoutCheck', sonuc[0][1])
