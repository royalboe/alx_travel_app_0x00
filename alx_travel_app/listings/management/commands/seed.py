import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from alx_travel_app.listings.models import User, Listing, Booking, Reviews

class Command(BaseCommand):
    help = 'Seeding for application data'

    def handle(self, *args, **options):
        # Get or create superuser
        users = User.objects.all()
        if len(users) < 4:
            usernames = ['Ayomide', 'Admin', 'Test', 'Gogo']
            for i in range(4):
                users.append(User.objects.create_superuser(username=usernames[i], password='test'))

            # create products - name, desc, price, stock, image
        listings = [
            Listing(name="Snowy Palace", description=lorem_ipsum.paragraph(), price=Decimal('12.99')),
            Listing(name="The Wall House", description=lorem_ipsum.paragraph(), price=Decimal('70.99')),
            Listing(name="Velvet Underground & Nico", description=lorem_ipsum.paragraph(), price=Decimal('15.99')),
            Listing(name="Enter the Wu-Tang (36 Chambers)", description=lorem_ipsum.paragraph(),
                    price=Decimal('17.99')),
            Listing(name="Palace Watch", description=lorem_ipsum.paragraph(), price=Decimal('350.99')),
            Listing(name="Pier Place", description=lorem_ipsum.paragraph(), price=Decimal('500.05')),
        ]

        Listing.objects.bulk_create(listings)
        listings = Listing.objects.all()