from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, Order
from .serializers import CartSerializer, CartItemAddSerializer, CheckoutSerializer, OrderSerializer, \
    TrackOrderSerializer
from .utils import convert_cart_to_order, send_order_confirmation_email
from django.conf import settings
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='add_item')
    def add_item(self, request):
        user = request.user
        serializer = CartItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        cart, created = Cart.objects.get_or_create(user=user, status='active')
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            if quantity > 0:
                total_price = product.price * quantity
                cart_item.quantity = quantity
                cart_item.unit_price = product.price
                cart_item.total_price = total_price
                cart_item.save()
            else:
                cart_item.delete()
        else:
            if quantity > 0:
                total_price = product.price * quantity
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,
                    total_price=total_price
                )

        if cart.cart_items.exists():
            cart.grand_total = sum(item.total_price for item in cart.cart_items.all())
            cart.save()
        else:
            cart.delete()
            return Response({"message": "Cart is empty and has been deleted."}, status=status.HTTP_204_NO_CONTENT)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        user = request.user
        serializer = CheckoutSerializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        shipping_address = serializer.validated_data['shipping_address']
        cart = Cart.objects.filter(user=user, status='active').first()

        order = convert_cart_to_order(cart, shipping_address)

        return Response({"message": "Order created successfully.", "order_id": order.id},
                        status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def pay_order(self, request, pk=None):
        try:
            order = self.get_object()
            charge = stripe.Charge.create(
                amount=int(order.grand_total * 100),
                currency='usd',
                source=request.data.get('stripe_token'),
                description=f"Charge for Order #{order.id}"
            )
            order.payment_status = 'completed'
            order.save()
            send_order_confirmation_email(order.id, order.user.email)
            return Response({"message": "Payment successful", "order_id": order.id}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def track_order(self, request):
        serializer = TrackOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_number = serializer.validated_data['order_number']
        order = Order.objects.filter(id=order_number).first()
        if order:
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

