from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from apps.order.models import Order


@shared_task(name='send_confirmation_email')
def send_order_confirmation_email():
    for order in Order.objects.filter(status='completed', is_send_email=False).order_by('created_at')[:10]:
        if order.user.email:
            send_mail(
                subject=f'Payment Confirmation for Order #{order.id}',
                message=f'Thank you for your payment. Your order #{order.id} has been successfully processed.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=False,
            )
            order.is_send_email = True
            order.save()
