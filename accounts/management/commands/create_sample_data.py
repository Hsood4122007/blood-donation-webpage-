from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import User
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample data for demonstration purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of sample users to create'
        )
        parser.add_argument(
            '--requests',
            type=int,
            default=20,
            help='Number of sample blood requests to create'
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@bloodplatform.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                user_type='admin',
                is_verified=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created admin user: admin/admin123')
            )

        # Sample data
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
        hospitals = ['City Hospital', 'Medical Center', 'General Hospital', 'Specialty Clinic', 'Community Hospital']
        
        # Mumbai coordinates (approximate center)
        mumbai_lat, mumbai_lon = 19.0760, 72.8777
        
        # Create sample donors
        created_users = 0
        for i in range(options['users']):
            username = f'donor{i+1}'
            if User.objects.filter(username=username).exists():
                continue
                
            # Generate random location within Mumbai (approx 50km radius)
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)
            
            user = User.objects.create_user(
                username=username,
                email=f'donor{i+1}@example.com',
                password='donor123',
                first_name=f'Donor{i+1}',
                last_name='Test',
                user_type='donor',
                phone_number=f'+9198765432{i:02d}',
                blood_group=random.choice(blood_groups),
                date_of_birth=datetime(1990, 1, 1) + timedelta(days=random.randint(0, 365*30)),
                is_verified=True,
                is_available=True,
                privacy_level='public',
                city=random.choice(cities),
                state='Maharashtra',
                country='India',
                latitude=mumbai_lat + lat_offset,
                longitude=mumbai_lon + lon_offset,
                has_medical_conditions=False,
                consent_given=True,
                data_retention_consent=True
            )
            created_users += 1
            
        self.stdout.write(
            self.style.SUCCESS(f'Created {created_users} sample donors')
        )

        # Create sample hospital users
        hospital_users = []
        for i, city in enumerate(cities[:5]):
            username = f'hospital{i+1}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'hospital{i+1}@{city.lower().replace(" ", "")}.com',
                    password='hospital123',
                    first_name=f'{random.choice(hospitals)} {city}',
                    user_type='hospital',
                    phone_number=f'+9198300000{i:02d}',
                    city=city,
                    state='Maharashtra',
                    country='India',
                    is_verified=True,
                    consent_given=True
                )
                hospital_users.append(user)

        self.stdout.write(
            self.style.SUCCESS(f'Created {len(hospital_users)} hospital users')
        )

        # Create sample blood requests
        from requests.models import BloodRequest
        import pytz
        
        created_requests = 0
        for i in range(min(options['requests'], len(hospital_users) * 4)):
            hospital_user = random.choice(hospital_users)
            
            # Generate random location near hospital city
            city_coords = {
                'Mumbai': (19.0760, 72.8777),
                'Delhi': (28.7041, 77.1025),
                'Bangalore': (12.9716, 77.5946),
                'Hyderabad': (17.3850, 78.4867),
                'Chennai': (13.0827, 80.2707)
            }
            
            city = hospital_user.city
            lat, lon = city_coords.get(city, (19.0760, 72.8777))
            lat_offset = random.uniform(-0.1, 0.1)
            lon_offset = random.uniform(-0.1, 0.1)
            
            # Random priority and blood group
            priority = random.choices(['normal', 'urgent', 'emergency'], weights=[60, 30, 10])[0]
            blood_group = random.choice(blood_groups)
            
            # Required by date (within next 7 days)
            required_by = datetime.now(pytz.UTC) + timedelta(
                days=random.randint(1, 7),
                hours=random.randint(1, 23)
            )
            
            request = BloodRequest.objects.create(
                requester=hospital_user,
                patient_name=f'Patient {i+1}',
                patient_age=random.randint(18, 80),
                patient_blood_group=blood_group,
                required_units=random.randint(1, 4),
                priority=priority,
                status='approved',  # Pre-approve for demo
                requester_type='hospital',
                reason='Medical emergency requiring blood transfusion',
                required_by=required_by,
                is_critical=random.choice([True, False]),
                hospital_name=hospital_user.first_name,
                city=city,
                state='Maharashtra',
                country='India',
                latitude=lat + lat_offset,
                longitude=lon + lon_offset,
                contact_person=hospital_user.first_name,
                contact_phone=hospital_user.phone_number,
                contact_email=hospital_user.email,
                approved_by=User.objects.get(username='admin'),
                approved_at=datetime.now(pytz.UTC)
            )
            created_requests += 1

        self.stdout.write(
            self.style.SUCCESS(f'Created {created_requests} sample blood requests')
        )

        # Summary
        total_users = User.objects.count()
        total_requests = BloodRequest.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(f'\n--- SUMMARY ---')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total Users: {total_users}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total Blood Requests: {total_requests}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Admin Login: admin / admin123')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Donor Login: donor1 / donor123')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Hospital Login: hospital1 / hospital123')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Access admin at: http://localhost:8000/admin/')
        )
