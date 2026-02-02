from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator
from auditlog.registry import auditlog

class User(AbstractUser):
    """Extended User model for blood donation platform"""
    
    USER_TYPE_CHOICES = [
        ('donor', 'Blood Donor'),
        ('hospital', 'Hospital Representative'),
        ('admin', 'System Administrator'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A Positive'),
        ('A-', 'A Negative'),
        ('B+', 'B Positive'),
        ('B-', 'B Negative'),
        ('AB+', 'AB Positive'),
        ('AB-', 'AB Negative'),
        ('O+', 'O Positive'),
        ('O-', 'O Negative'),
    ]
    
    # Core fields
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='donor')
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        blank=True,
        null=True
    )
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    last_donation_date = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    privacy_level = models.CharField(
        max_length=10,
        choices=[('public', 'Public'), ('private', 'Private')],
        default='public'
    )
    
    # Location fields
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Medical information
    has_medical_conditions = models.BooleanField(default=False)
    medical_conditions = models.TextField(blank=True)
    last_medical_checkup = models.DateField(blank=True, null=True)
    
    # GDPR compliance fields
    consent_given = models.BooleanField(default=False)
    data_retention_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_eligible_donor(self):
        """Check if user is eligible to donate blood"""
        if self.user_type != 'donor' or not self.is_verified:
            return False
        
        if self.has_medical_conditions:
            return False
            
        if self.last_donation_date:
            # Minimum 3 months between donations
            return (timezone.now().date() - self.last_donation_date).days >= 90
        
        return True
    
    @property
    def days_since_last_donation(self):
        """Return days since last donation"""
        if self.last_donation_date:
            return (timezone.now().date() - self.last_donation_date).days
        return None

# Audit logging for compliance
auditlog.register(User)