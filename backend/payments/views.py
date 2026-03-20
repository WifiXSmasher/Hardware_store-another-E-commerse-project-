from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 

from cart.models import CartItem
import razorpay
from payments.razorpay_client import client
# Create your views here.

class CreateRazorpayOrder(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        cart_items = CartItem.objects.filter(cart__user=request.user)

        if not cart_items.exists():
            return Response({"error" : "Cart Empty"})
        
        total  = 0 

        for item in cart_items:

            if item.product:
                
                total += item.product.price * item.quantity

            elif item.spare_part:

                total += item.spare_part.price * item.quantity

        

        amount_paise = int(total*100)

        razorpay_order = client.order.create({
            "amount" : amount_paise,
            "currency" : "INR",
            "payment_capture" : '0'
        })

        return Response({
            "razorpay_order_id" : razorpay_order["id"],
            "amount" : amount_paise
        })