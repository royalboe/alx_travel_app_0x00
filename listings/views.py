# from django.shortcuts import render

# from rest_framework import request, JsonResponse
from django.http import JsonResponse
from .models import User, Listing, Booking, Reviews
from .serializers import ListingSerializer
# Create your views here.

def listing_list(request):
    listings = Listing.objects.all()
    serializer = ListingSerializer(listings, many=True)
    return JsonResponse({'data': serializer.data}, safe=False)