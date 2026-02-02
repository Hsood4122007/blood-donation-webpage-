from django.db import models
from django.utils import timezone
from accounts.models import User
from auditlog.registry import auditlog

class BloodRequest(models.Model):
    """Blood request from hospitals/patients"""
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('active', 'Active - Seeking Donors'),
        ('partially_fulfilled', 'Partially Fulfilled'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    REQUESTER_TYPE_CHOICES = [
        ('hospital', 'Hospital'),
        ('individual', 'Individual Patient'),
        ('relative', 'Patient Relative'),
    ]
    
    # Core fields
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=200)
    patient_age = models.IntegerField()
    patient_blood_group = models.CharField(max_length=3)
    required_units = models.IntegerField(default=1)
    fulfilled_units = models.IntegerField(default=0)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requester_type = models.CharField(max_length=10, choices=REQUESTER_TYPE_CHOICES, default='hospital')
    
    # Medical details
    reason = models.TextField()
    required_by = models.DateTimeField()
    medical_certificate = models.FileField(upload_to='medical_certificates/', blank=True, null=True)
    is_critical = models.BooleanField(default=False)
    
    # Location
    hospital_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='India')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Contact information
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    
    # Approval workflow
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='approved_requests')
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['city', 'patient_blood_group']),
        ]
    
    def __str__(self):
        return f"Request #{self.id} - {self.patient_blood_group} - {self.hospital_name}"
    
    def save(self, *args, **kwargs):
        # Set expiration time (7 days from required_by for normal, 3 days for urgent, 1 day for emergency)
        if not self.expires_at:
            if self.priority == 'emergency':
                self.expires_at = self.required_by + timezone.timedelta(days=1)
            elif self.priority == 'urgent':
                self.expires_at = self.required_by + timezone.timedelta(days=3)
            else:
                self.expires_at = self.required_by + timezone.timedelta(days=7)
        
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @property
    def remaining_units(self):
        return self.required_units - self.fulfilled_units
    
    @property
    def completion_percentage(self):
        if self.required_units == 0:
            return 0
        return (self.fulfilled_units / self.required_units) * 100

class RequestMatch(models.Model):
    """Match between blood request and donor"""
    
    STATUS_CHOICES = [
        ('proposed', 'Proposed to Donor'),
        ('accepted', 'Donor Accepted'),
        ('declined', 'Donor Declined'),
        ('completed', 'Donation Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='matches')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_matches')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='proposed')
    proposed_at = models.DateTimeField(default=timezone.now)
    responded_at = models.DateTimeField(null=True, blank=True)
    donation_scheduled_at = models.DateTimeField(null=True, blank=True)
    donation_completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # Matching details
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    compatibility_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ['request', 'donor']
        ordering = ['-proposed_at']
    
    def __str__(self):
        return f"Match: {self.request.id} - {self.donor.username} ({self.status})"

class RequestUpdate(models.Model):
    """Track updates and status changes for requests"""
    
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status_from = models.CharField(max_length=20, choices=BloodRequest.STATUS_CHOICES)
    status_to = models.CharField(max_length=20, choices=BloodRequest.STATUS_CHOICES)
    notes = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Request {self.request.id}: {self.status_from} → {self.status_to}"

# Register for audit logging
auditlog.register(BloodRequest)
auditlog.register(RequestMatch)
auditlog.register(RequestUpdate)