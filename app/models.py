import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Seller is linked to Django User model
    location = models.CharField(max_length=255, blank=True, null=True)  # Optionally track location
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Product image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    def save(self, *args, **kwargs):
        # Check if the user already has a profile picture
        if self.pk:  # This is an existing user
            old_picture = Profile.objects.get(pk=self.pk).profile_picture
            if old_picture != self.profile_picture:
                old_path = old_picture.path
                if old_picture.name != 'profile_pics/default.png':
                    os.remove(old_path)

        super().save(*args, **kwargs)  # Call the parent class's save method

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
