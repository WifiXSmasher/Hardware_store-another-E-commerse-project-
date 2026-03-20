from django.shortcuts import render
# Create your views here.
from django.db import transaction


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import CartItem
from cart.views import get_user_cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


from django.core.mail import send_mail
from django.conf import settings
from products.models import SparePart,Product# to make it atomic 
class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # cart_items = CartItem.objects.filter(cart__user=request.user)
        # this will prevent multiple checkout for the same user 
        with transaction.atomic():
            cart_items = CartItem.objects.select_for_update().filter(cart__user=request.user)
            if not cart_items.exists():
                return Response({"error": "Cart is empty"}, status=400)


            total = 0

            # Lock spare part rows
            spare_part_ids = [
                item.spare_part.id
                for item in cart_items
                if item.spare_part is not None
            ]

            spare_parts = SparePart.objects.select_for_update().filter(
                id__in=spare_part_ids
            )

            spare_part_map = {sp.id: sp for sp in spare_parts}


            # Lock products
            product_ids = [
                item.product.id
                for item in cart_items
                if item.product is not None
            ]

            products = Product.objects.select_for_update().filter(
                id__in=product_ids
            )

            product_map = {p.id: p for p in products}

            # calculate total 
            for item in cart_items:

                if item.product:
                    product = product_map[item.product.id]# fro atomicity 

                    if item.product.stock < item.quantity:
                        return Response(
                            {"error" : f"not enough stock for the {item.product.name}"},
                            status=400,
                        )
                    total += item.product.price * item.quantity

                elif item.spare_part:
                    if item.spare_part.stock < item.quantity:
                        return Response(
                            {"error" : f"not enough stock for the {item.spare_part.name}"},
                            status=400,
                        )
                    total += item.spare_part.price * item.quantity

            # create order hmmmm........
            order = Order.objects.create(
                user=request.user,
                total_amount=total
            )

            # uodate stock and create order
            for item in cart_items:

                # PRODUCT
                if item.product:

                    product = product_map[item.product.id]

                    if product.stock < item.quantity:
                        return Response({
                            "error": f"Not enough stock for {product.name}"
                        }, status=400)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price
                    )

                    product.stock -= item.quantity
                    product.save()

                # SPARE PART
                elif item.spare_part:

                    spare_part = spare_part_map[item.spare_part.id]

                    if spare_part.stock < item.quantity:
                        return Response({
                            "error": f"Not enough stock for {spare_part.name}"
                        }, status=400)

                    OrderItem.objects.create(
                        order=order,
                        spare_part=spare_part,
                        quantity=item.quantity,
                        price=spare_part.price
                    )

                    spare_part.stock -= item.quantity
                    spare_part.save()

            #clear the cart after the order 
            cart_items.delete()

            # confirmation email
            send_mail(
                subject="Order Confirmation",
                message=f"""
Hello {request.user.username},

Your order #{order.id} has been successfully placed.

Total Amount: {total}

""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )

        return Response({
            "message": "Order created",
            "order_id": order.id,
            "total": total
        })


from rest_framework import generics


class OrderListView(generics.ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderDetailView(generics.RetrieveAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)