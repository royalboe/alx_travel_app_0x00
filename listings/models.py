from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    user_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)  # This is the primary key of the model

class Listing(models.Model):
    class Currency(models.TextChoices):
        NGN = 'NGN', 'Nigerian Naira (NGN)'
        USD = 'USD', 'US Dollar (USD)'
        EUR = 'EUR', 'Euro (EUR)'
        GBP = 'GBP', 'British Pound (GBP)'
        CAD = 'CAD', 'Canadian Dollar (CAD)'
        AUD = 'AUD', 'Australian Dollar (AUD)'
        JPY = 'JPY', 'Japanese Yen (JPY)'
        ZAR = 'ZAR', 'South African Rand (ZAR)'
    listing_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False) # This is the primary key of the mode
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    currency = models.CharField(max_length=3,
        choices=Currency.choices,
        default=Currency.NGN
        )
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    def average_rating(self):
        return Reviews.objects.filter(booking__listing=self).aggregate(avg_rating=models.Avg('rating'))['avg_rating']

    def __str__(self):
        return self.name

class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    booking_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    # def ordered_by(self):
    #     return self.created_at

    def __str__(self):
        return f'Booking {self.booking_id} was made by {self.user.username} on listing {self.listing.name} on {self.created_at.strftime("%Y-%m-%d")}'


class Reviews(models.Model):
    review_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='review')
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'Review by {self.user.username} - {self.rating} stars'
