from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    currency = models.CharField(max_length=3, default='NGN')

    def __str__(self):
        return self.name

class Booking(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    booking_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f'Booking {self.booking_id} was made by {self.user.username} on listing {self.listing.name} on {self.created_at}'


class Reviews(models.Model):
    review_id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for Booking {self.booking.booking_id} - Rating: {self.rating}'
