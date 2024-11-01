from django.contrib.auth import get_user_model
from django.db import models

from apps.product.models import Product

# Create your models here.

User = get_user_model()


class Cart(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('ordered', 'Ordered')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('shipped', 'Shipped'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    shipping_address = models.TextField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='pending', choices=PAYMENT_STATUS)
    is_send_email = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
