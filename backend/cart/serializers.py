# from rest_framework import serializers
# from .models import CartItem
# from products.models import SparePart
# from rest_framework import serializers
# from .models import CartItem
# from products.models import SparePart

# class CartItemSerializer(serializers.ModelSerializer):

#     spare_part_name = serializers.CharField(
#         source = "spare_part.name",
#         read_only = True,
#     )

#     price = serializers.DecimalField(
#         source = "spare_part.price",
#         max_digits=10,
#         decimal_places=2,
#         read_only = True 
#     )

#     class Meta : 
#         model = CartItem 
#         fields = [
#             "id",
#             "spare_part",
#             "spare_part_name",
#             "price",
#             "quantity",
#         ]    



from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "item_type",
            "name",
            "price",
            "quantity",
        ]

    def get_name(self, obj):

        if obj.product:
            return obj.product.name

        if obj.spare_part:
            return obj.spare_part.name

        return None

    def get_price(self, obj):

        if obj.product:
            return obj.product.price

        if obj.spare_part:
            return obj.spare_part.price

        return None

    def get_item_type(self, obj):

        if obj.product:
            return "product"

        if obj.spare_part:
            return "spare_part"

        return None