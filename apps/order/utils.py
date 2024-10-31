from django.conf import settings
from django.core.mail import send_mail

from .models import Order, OrderItem


def convert_cart_to_order(cart, shipping_address):
    order = Order.objects.create(
        user=cart.user,
        grand_total=cart.grand_total,
        status='pending',
        shipping_address=shipping_address
    )
    for cart_item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            total_price=cart_item.total_price
        )
        product = cart_item.product
        product.quantity -= cart_item.quantity
        product.save()
    cart.status = 'ordered'
    cart.save()

    return order


def send_order_confirmation_email(order_id, user_email):
    send_mail(
        subject=f'Payment Confirmation for Order #{order_id}',
        message=f'Thank you for your payment. Your order #{order_id} has been successfully processed.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )
