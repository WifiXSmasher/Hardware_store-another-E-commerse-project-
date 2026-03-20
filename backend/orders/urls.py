from django.urls import path
from .views import CheckoutView, OrderListView, OrderDetailView


urlpatterns = [

    path("checkout/", CheckoutView.as_view()),

    path("", OrderListView.as_view()),

    path("<int:pk>/", OrderDetailView.as_view()),

]