from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
        )

    created_at = models.DateTimeField(auto_now_add=True)
    stock = models.IntegerField(default=0)# to allow buying the product 
    
    def __str__(self):
        return self.name
    
class SparePart(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="spare_parts"
    )

    name =models.CharField( max_length=255)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    stock = models.PositiveIntegerField()
    image = models.ImageField( upload_to="products/spare_parts",)

    def __str__(self):
        return self.name 
    
class ProductImage(models.Model):
    product  = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    
    image =models.ImageField(
        upload_to="products/"
        )
    
    def __str__(self):
        return f"Image for {self.product.name}"