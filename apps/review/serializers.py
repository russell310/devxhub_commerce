from rest_framework import serializers

from .models import Review
from ..order.models import Order, OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['user', 'product', 'review', 'created_at']
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']
        exists = OrderItem.objects.filter(order__user=user, product=product, order__status='completed').exists()
        if not exists:
            raise serializers.ValidationError({'product': 'Review not allowed for this product'})
        return attrs
