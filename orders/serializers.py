from rest_framework import serializers
from .models import User, Driver, Order

class OrderSerializer(serializers.ModelSerializer):
    class meta:
        model = Order
        fields = ['id', 'customer', 'driver', 'status', 'pickup_coords', 'dropoff_coords', 'price', 'distance', 'duration']