from django.db import models
from django.conf import settings
from products.models import SparePart , Product # to allow buying the product too 

User = settings.AUTH_USER_MODEL
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending","Pending"),
        ("paid", "Paid"),
        ("fialed" , "Failed"),
    ]

    user = models.ForeignKey(
        User , 
        on_delete=models.CASCADE,
        related_name="orders",
    )
    
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    def __str__(self):
        return f"order{self.id}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(#to allow buying the product too 
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    
    spare_part = models.ForeignKey(
        SparePart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    
    quantity = models.PositiveIntegerField()
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.spare_part.name} x {self.quantity}"