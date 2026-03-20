from django.shortcuts import render
from .models import Cart

# Create your views here.
def get_user_cart(user):
    cart,created = Cart.objects.get_or_create(user=user)
    return cart


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart  = get_user_cart(request.user)
        items  = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(items , many =True)

        return Response(serializer.data)
    

# class AddToCartView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request):

#         spare_part_id = request.data.get("spare_part")
#         quantity = int(request.data.get("quantity", 1))

#         cart = get_user_cart(request.user)

#         spare_part = SparePart.objects.get(id=spare_part_id)

#         item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             spare_part=spare_part
#         )

#         if not created:
#             item.quantity += quantity
#         else:
#             item.quantity = quantity

#         item.save()

#         return Response({"message": "Item added to cart"})

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CartItem
from products.models import SparePart,Product
from .views import get_user_cart


class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        spare_part_id = request.data.get("spare_part_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        cart = get_user_cart(request.user)

        if product_id and spare_part_id:
            return Response(
                {"error": "Send either product_id or spare_part_id"},
                status=400
            )
        # PRODUCT CASE
        if product_id:# to make the product available too 

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if product.stock <= 0 :
                return Response(
                    {"error" : "Product not available",},
                    status = 400 ,
                )

            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product
            )

        # SPARE PART CASE
        elif spare_part_id:

            try:
                spare_part = SparePart.objects.get(id=spare_part_id)
            except SparePart.DoesNotExist:
                return Response(
                    {"error": "Spare part not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            if spare_part.stock <= 0 :
                return Response(
                    {"error" : "Spare part not available",},
                    status = 400 ,
                )
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                spare_part=spare_part
            )

        else:
            return Response(
                {"error": "product_id or spare_part_id required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # UPDATE QUANTITY
        # if not created:
        #     item.quantity += quantity
        # else:
                #     item.quantity = quantity
        new_quantity = item.quantity + quantity if not created else quantity

        # PRODUCT CHECK
        if item.product and new_quantity > item.product.stock:
            return Response(
                {"error": "Not enough stock available"},
                status=400
            )

        # SPARE PART CHECK
        if item.spare_part and new_quantity > item.spare_part.stock:
            return Response(
                {"error": "Not enough stock available"},
                status=400
            )

        item.quantity = new_quantity

        item.save()

        return Response({"message": "Item added to cart"})

class RemoveFromCartView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):

        cart = get_user_cart(request.user)

        item = CartItem.objects.get(id=item_id, cart=cart)

        item.delete()

        return Response({"message": "Item removed"})