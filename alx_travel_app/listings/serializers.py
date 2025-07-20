from .models import User, Listing, Booking, Reviews
from rest_framework import serializers

class ListingSerializer(serializers.ModelSerializer):
    host_name = serializers.CharField(source='host.username')

    class Meta:
        model = Listing
        fields = [
            'id',
            'name',
            'location',
            'description',
            'price',
            'created_at',
            'currency',
            'host_name'
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'