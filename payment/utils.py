import json
from .models import *
from wholesale.utils import *
from store.utils import *
import iyzipay

options = {
    'api_key': 'api_key',
    'secret_key': 'secret_key',
    'base_url': 'base_url'
}

def checker(token,payment):
    try:
        paymentkey, created = PaymentKey.objects.get_or_create(id=1)
    except PaymentKey.DoesNotExist:
        paymentkey = None

    if paymentkey:
        api_key = paymentkey.api_key
        secret_key = paymentkey.secret_key
        base_url = paymentkey.base_url

        options = {
            'api_key': api_key,
            'secret_key': secret_key,
            'base_url': base_url
        }

    request = dict([('locale', 'tr')])
    request['conversationId'] = str(payment.conversationId)
    request['token'] = str(token)
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    result = checkout_form_result.read().decode('utf-8')
    sonuc = json.loads(result, object_pairs_hook=list)
    check = 'İşlem Başarısız'
    return sonuc
