from django.contrib import admin
from .models import Product, SparePart, ProductImage

# Register your models here.
admin.site.register(Product)
admin.site.register(SparePart)
admin.site.register(ProductImage)
