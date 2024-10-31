from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from ..product.models import Product


class CartItemAddSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=0)

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']

        if product.quantity < quantity:
            raise serializers.ValidationError("Requested quantity exceeds available stock.")
        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = CartItem
        fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'grand_total', 'status', 'cart_items']


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()

    def validate(self, attrs):
        cart = Cart.objects.filter(user=self.context['request'].user, status='active').first()
        if not cart or not cart.cart_items.exists():
            raise serializers.ValidationError("No active cart. Please add items")
        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'grand_total', 'status', 'order_items', 'shipping_address',
                  'payment_status']


class TrackOrderSerializer(serializers.Serializer):
    order_number = serializers.CharField()
