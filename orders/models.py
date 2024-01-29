from django.db import models
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class Driver(models.Model):
    #the docs that a driver should inform
    motorcycle_card = models.FileField(upload_to='uploads/')
    national_card = models.FileField(upload_to='uploads/')


class Order(models.Model):
    #customers known as an order
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pickup_coords = models.CharField(max_length=100)
    dropoff_coords = models.CharField(max_length=100)
    
