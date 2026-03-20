from django.urls import path
from .views import CreateRazorpayOrder

urlpatterns = [
    path("create-order/", CreateRazorpayOrder.as_view()),
]