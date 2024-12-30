from django.db import models
from django.contrib.auth.models import AbstractUser

class ClothingItem(models.Model):
    image = models.ImageField(upload_to='clothing_images/')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    availability = models.BooleanField(default=True)

class AdditionalImage(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='additional_images/')

class Status(models.Model):
    ORDERED = 'Ordered'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'

    STATUS_CHOICES = [
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]
    order_status= models.CharField(max_length=50, choices=STATUS_CHOICES)

class Order(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, related_name='orders',on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    quantity = models.IntegerField()
    contact_number = models.CharField(max_length=20)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)

from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, default='NoAddress')
    is_admin = models.BooleanField(default=False)
