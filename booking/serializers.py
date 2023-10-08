from rest_framework import serializers
from .models import *
class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields ='__all__'


class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['created_at', 'bus', 'route', 'status']

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Payment
        fields = '__all__'