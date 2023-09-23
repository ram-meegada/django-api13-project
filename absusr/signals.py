from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import order
from django.dispatch import receiver

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('ipn valid')
    ipn = sender
    if ipn.payment_status == 'Completed':
        order.objects.create()

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('invalid ipn')
    ipn = sender
    if ipn.payment_status == 'Completed':
        order.objects.create()