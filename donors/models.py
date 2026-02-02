from django.db import models
from django.utils import timezone
from accounts.models import User
from auditlog.registry import auditlog

class DonorHistory(models.Model):
    """Track donor's blood donation history"""
    
    DONATION_TYPE_CHOICES = [
        ('whole_blood', 'Whole Blood'),
        ('plasma', 'Plasma'),
        ('platelets', 'Platelets'),
    ]
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donation_history')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES, default='whole_blood')
    donation_date = models.DateTimeField(default=timezone.now)
    hospital = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3)
    volume_ml = models.IntegerField(default=450)  # Standard blood donation volume
    hemoglobin_level = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    is_successful = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-donation_date']
        verbose_name_plural = 'Donor Histories'
    
    def __str__(self):
        return f"{self.donor.username} - {self.donation_date.strftime('%Y-%m-%d')}"

class DonorAvailability(models.Model):
    """Track donor availability status"""
    
    donor = models.OneToOneField(User, on_delete=models.CASCADE, related_name='availability')
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    reason_unavailable = models.TextField(blank=True)
    available_from = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.donor.username} - {'Available' if self.is_available else 'Unavailable'}"

class DonorRating(models.Model):
    """Track donor reliability and ratings"""
    
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField(blank=True)
    donation_id = models.ForeignKey(DonorHistory, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['donor', 'rated_by', 'donation_id']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.donor.username} - {self.rating} stars"

# Register models for audit logging
auditlog.register(DonorHistory)
auditlog.register(DonorAvailability)
auditlog.register(DonorRating)