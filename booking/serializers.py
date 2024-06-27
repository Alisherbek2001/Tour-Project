from rest_framework import serializers
from .models import Booking
from tour.serializers import TourSerializer

class BookingSerializer(serializers.ModelSerializer):
    tour = TourSerializer()
    class Meta:
        model = Booking
        fields = '__all__'