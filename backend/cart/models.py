from django.db import models
from django.conf import settings 
from products.models import SparePart ,Product #to allow buying the product too 



User = settings.AUTH_USER_MODEL
# Create your models here.
class Cart(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name = "items",
    ) 
    
    spare_part = models.ForeignKey(
        SparePart,
        #added null and blank cause the product cant be added wothout it .
        null = True ,
        blank = True ,                     
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(# to allow buying the product too 
        Product,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default= 1 )

    added_at = models.DateTimeField( auto_now_add=True)

    class Meta : 
        unique_together = ("cart","spare_part")

    def __str__(self):
        return f"{self.spare_part.name} x {self.quantity}"
    
    