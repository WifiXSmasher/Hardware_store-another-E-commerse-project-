from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated   
# from rest_framework import APIView 
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import generics
from .serializers import RegisterSerializer

# Create your views here.
from .models import User    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

from django.utils.http import urlsafe_base64_decode

from .serializers import PasswordResetSerializer
from django.contrib.auth.tokens import default_token_generator

class PasswordResetRequestView(APIView):

    def post(self, request):

        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Password reset email sent"
            })

        return Response(serializer.errors, status=400)
    
class PasswordResetConfirmView(APIView):

    def post(self, request):

        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)
        except:
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful"})