from django.db import models
from django.utils import timezone
from accounts.models import User
from requests.models import BloodRequest
from auditlog.registry import auditlog

class Notification(models.Model):
    """User notifications system"""
    
    TYPE_CHOICES = [
        ('request_match', 'Blood Request Match'),
        ('request_update', 'Request Status Update'),
        ('donation_reminder', 'Donation Reminder'),
        ('system_alert', 'System Alert'),
        ('verification', 'Account Verification'),
        ('admin_message', 'Admin Message'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_request = models.ForeignKey(BloodRequest, on_delete=models.SET_NULL, 
                                      null=True, blank=True, related_name='notifications')
    
    # Status tracking
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery tracking
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    push_sent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['notification_type', 'priority']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def save(self, *args, **kwargs):
        # Set default expiration (30 days)
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=30)
        super().save(*args, **kwargs)

class EmailTemplate(models.Model):
    """Email templates for notifications"""
    
    TEMPLATE_CHOICES = [
        ('donor_match', 'Donor Match Notification'),
        ('request_approved', 'Request Approved'),
        ('request_fulfilled', 'Request Fulfilled'),
        ('donation_reminder', 'Donation Reminder'),
        ('verification_code', 'Email Verification'),
        ('password_reset', 'Password Reset'),
        ('emergency_alert', 'Emergency Blood Request'),
    ]
    
    template_name = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, unique=True)
    subject = models.CharField(max_length=200)
    body_html = models.TextField()
    body_text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_template_name_display()

class NotificationPreference(models.Model):
    """User notification preferences"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_requests = models.BooleanField(default=True)
    email_reminders = models.BooleanField(default=True)
    email_system = models.BooleanField(default=True)
    
    # SMS preferences
    sms_requests = models.BooleanField(default=False)
    sms_reminders = models.BooleanField(default=False)
    
    # Push preferences
    push_requests = models.BooleanField(default=True)
    push_reminders = models.BooleanField(default=True)
    
    # Emergency overrides
    emergency_sms = models.BooleanField(default=True)
    emergency_push = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"

class NotificationLog(models.Model):
    """Track notification delivery attempts"""
    
    DELIVERY_METHOD_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
    ]
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery_logs')
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    recipient = models.CharField(max_length=255)  # Email or phone number
    error_message = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.delivery_method} to {self.recipient} - {self.status}"

# Register for audit logging
auditlog.register(Notification)
auditlog.register(EmailTemplate)
auditlog.register(NotificationPreference)
auditlog.register(NotificationLog)