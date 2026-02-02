from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                blood_group='O+',
                city='Delhi',
                state='Delhi',
                pincode='110001'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))
        
        # Create test donor
        if not User.objects.filter(username='testdonor').exists():
            donor = User.objects.create_user(
                username='testdonor',
                email='donor@example.com',
                password='donor123',
                first_name='Test',
                last_name='Donor',
                user_type='donor',
                blood_group='A+',
                city='Delhi',
                state='Delhi',
                pincode='110001',
                phone_number='+919876543210',
                is_verified=True,
                is_available=True
            )
            self.stdout.write(self.style.SUCCESS('Test donor created: testdonor/donor123'))

        self.stdout.write(self.style.SUCCESS('Test users created successfully!'))