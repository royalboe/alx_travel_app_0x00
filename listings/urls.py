from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('listings/', views.listing_list, name='listing-list'),
    # Add more URL patterns for other views as needed
]
