import random
from decimal import Decimal

from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
from django.utils import timezone, lorem_ipsum
from alx_travel_app.listings.models import User, Listing, Booking, Reviews



class Command(BaseCommand):
    help = 'Seeding for application data'

    def handle(self, *args, **options):
        # Get or create superuser
        usernames = ['Ayomide', 'Admin', 'Test', 'Gogo']
        if User.objects.count() < 4:
            for username in usernames:
                User.objects.create_user(username=username, password='test')
            self.stdout.write("Created 4 users.")

        users = list(User.objects.all())

        # Create listings
        if Listing.objects.count() == 0:
            sample_names = [
                "Snowy Palace", "The Wall House", "Velvet Underground & Nico",
                "Enter the Wu-Tang", "Palace Watch", "Pier Place"
            ]
            listings = []
            for name in sample_names:
                listing = Listing(
                    name=name,
                    description=lorem_ipsum.paragraph(),
                    price=Decimal(random.uniform(20.00, 500.00)).quantize(Decimal('0.01')),
                    location=random.choice(['Lagos', 'Abuja', 'Ibadan', 'Enugu', 'Kano']),
                    host=random.choice(users),
                    currency='NGN',
                )
                listings.append(listing)

            Listing.objects.bulk_create(listings)
            self.stdout.write(f"Created {len(listings)} listings.")

        listings = list(Listing.objects.all())

        # Create bookings
        if Booking.objects.count() == 0:
            bookings = []
            for _ in range(10):
                booking = Booking(
                    status=random.choice(Booking.StatusChoices.values),
                    listing=random.choice(listings),
                    user=random.choice(users),
                    created_at=timezone.now()
                )
                bookings.append(booking)

            Booking.objects.bulk_create(bookings)
            self.stdout.write(f"Created {len(bookings)} bookings.")

        bookings = list(Booking.objects.all())

        # Create reviews
        if Reviews.objects.count() == 0:
            reviews = []
            for booking in bookings[:5]:  # Limit to avoid OneToOne conflict
                review = Reviews(
                    booking=booking,
                    rating=random.randint(1, 5),
                    title=random.choice(['Nice', 'Okay', 'Perfect', 'Could be better', 'Loved it']),
                    user=booking.user
                )
                reviews.append(review)

            Reviews.objects.bulk_create(reviews)
            self.stdout.write(f"Created {len(reviews)} reviews.")

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))