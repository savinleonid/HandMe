from django.db import models
from django.contrib.auth.models import User

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Seller is linked to Django User model
    location = models.CharField(max_length=255, blank=True, null=True)  # Optionally track location
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Product image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
