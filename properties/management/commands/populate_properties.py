from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with sample properties for testing caching'

    def handle(self, *args, **options):
        # Sample properties data
        sample_properties = [
            {
                'title': 'Modern Downtown Apartment',
                'description': 'A beautiful 2-bedroom apartment in the heart of downtown with stunning city views.',
                'price': Decimal('2500.00'),
                'location': 'Downtown'
            },
            {
                'title': 'Cozy Suburban House',
                'description': 'A charming 3-bedroom house with a large backyard, perfect for families.',
                'price': Decimal('3200.00'),
                'location': 'Suburbs'
            },
            {
                'title': 'Luxury Penthouse',
                'description': 'An exclusive penthouse with panoramic views and premium amenities.',
                'price': Decimal('8500.00'),
                'location': 'Uptown'
            },
            {
                'title': 'Beach House Retreat',
                'description': 'A peaceful beach house just steps away from the ocean.',
                'price': Decimal('4200.00'),
                'location': 'Beachfront'
            },
            {
                'title': 'Urban Loft',
                'description': 'A trendy loft space in the arts district with exposed brick walls.',
                'price': Decimal('2800.00'),
                'location': 'Arts District'
            },
            {
                'title': 'Mountain Cabin',
                'description': 'A rustic cabin surrounded by nature, perfect for weekend getaways.',
                'price': Decimal('1800.00'),
                'location': 'Mountains'
            },
            {
                'title': 'Historic Brownstone',
                'description': 'A beautifully restored brownstone with original architectural details.',
                'price': Decimal('4500.00'),
                'location': 'Historic District'
            },
            {
                'title': 'Waterfront Condo',
                'description': 'A modern condo with direct water access and marina views.',
                'price': Decimal('3800.00'),
                'location': 'Waterfront'
            }
        ]

        created_count = 0
        for prop_data in sample_properties:
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                defaults=prop_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created property: {property_obj.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Property already exists: {property_obj.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new properties!')
        )
        self.stdout.write(
            f'Total properties in database: {Property.objects.count()}'
        )
