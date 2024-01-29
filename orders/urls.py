from django.urls import path
from .views import driver_orders, accept_order

urlpatterns = [
    path('driver_orders/', driver_orders, name='driverorders'),
    path('accept_order/', accept_order, name='acceptorder'),
]
