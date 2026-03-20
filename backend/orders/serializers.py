from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "name",
            "quantity",
            "price",
        ]

    def get_name(self, obj):

        if obj.product:
            return obj.product.name

        if obj.spare_part:
            return obj.spare_part.name

        return None


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "total_amount",
            "created_at",
            "items",
        ]