from django.shortcuts import render
from .models import User, Driver, Order
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests


def get_distance(lat1, lon1, lat2, lon2, api_key):
    #gets the coordinates of origin and the distance, send it to the address below and calculates the time_length and distance
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={lat1},{lon1}&destinations={lat2},{lon2}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['rows'][0]['elements'][0]['distance']['text'], data['rows'][0]['elements'][0]['duration']['text']


@csrf_exempt
def driver_orders(request):
    #sets the coordinates 
    if request.method == 'GET':
        orders = Order.objects.filter(status='pending').values()
        for order in orders:
            lat1, lon1 = order['pickup_coords'].split(',')
            lat2, lon2 = order['dropoff_coords'].split(',')
            #calls the func to calculate the duration and the distance
            distance, duration = get_distance(float(lat1), float(lon1), float(lat2), float(lon2), 'YOUR_API_KEY')
            order['distance'] = distance
            order['duration'] = duration
        return JsonResponse({'orders': list(orders)})
    elif request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.driver = request.user
        order.driver_name = request.user.first_name + " " + request.user.last_name
        order.car_number = 'ABC123' # set your own car number
        order.save()
        return JsonResponse({'message': 'Order selected successfully'})
    

@csrf_exempt
def accept_order(request):
    #shows the customer the price , and allow them to accept or deny
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        distance = order.distance
        duration = order.duration
        rate_per_mile = 2.0 # set your own rate
        rate_per_minute = 0.5 # set your own rate
        total_distance = float(distance[:-3]) * rate_per_mile
        total_time = int(duration[:-4]) * rate_per_minute
        order.price = max(total_distance, total_time)
        order.status = 'accepted'
        order.save()
        return JsonResponse({'message': 'Order accepted successfully'})


