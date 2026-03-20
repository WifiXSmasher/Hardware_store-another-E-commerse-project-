from rest_framework import serializers
from .models import Product, SparePart, ProductImage



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductImage
        fields = ["id", "image"]


class SparePartSerializer(serializers.ModelSerializer):

    class Meta :
        model = SparePart
        fields = ["id","name" , "price" , "stock" , "image"]


class ProductSerializer(serializers.ModelSerializer):
    spare_parts = SparePartSerializer(many = True , read_only=True)

    images  = ProductImageSerializer(many = True , read_only=True)

    class Meta : 
        model = Product 
        fields = [
            "id",
            "name",
            "brand",
            "description",
            "price",
            "spare_parts",
            "images",
            "stock",
        ]

        