from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from accounts.models import User
from requests.models import BloodRequest
from notifications.models import Notification
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_emergency_notifications(request_id):
    """Send emergency notifications to matching donors"""
    try:
        blood_request = BloodRequest.objects.get(id=request_id)
        
        # Import here to avoid circular imports
        from donors.matching import BloodMatcher
        
        # Find matching donors
        matching_donors = BloodMatcher.get_best_matching_donors(
            blood_group=blood_request.patient_blood_group,
            latitude=float(blood_request.latitude),
            longitude=float(blood_request.longitude),
            priority=blood_request.priority,
            limit=50
        )
        
        notifications_sent = 0
        for donor_data in matching_donors:
            donor = donor_data['donor']
            
            # Check donor preferences
            preferences = getattr(donor, 'notification_preferences', None)
            if preferences and not preferences.emergency_sms and not preferences.emergency_push:
                continue
            
            # Create notification
            notification = Notification.objects.create(
                user=donor,
                notification_type='request_match',
                priority='urgent' if blood_request.priority == 'emergency' else 'high',
                title=f"Emergency Blood Request - {blood_request.patient_blood_group}",
                message=f"""Urgent blood donation needed!
                
Patient: {blood_request.patient_name}
Blood Group: {blood_request.patient_blood_group}
Hospital: {blood_request.hospital_name}
City: {blood_request.city}
Required by: {blood_request.required_by.strftime('%Y-%m-%d %H:%M')}
Distance: {donor_data['donor'].distance_km} km

This is an emergency request. Your quick response can save a life!""",
                related_request=blood_request
            )
            
            # Send email notification
            if preferences is None or preferences.email_requests:
                send_email_notification.delay(notification.id)
            
            # Send SMS notification (if enabled)
            if preferences and preferences.sms_requests:
                send_sms_notification.delay(notification.id)
            
            notifications_sent += 1
        
        logger.info(f"Sent emergency notifications to {notifications_sent} donors for request {request_id}")
        return f"Notifications sent to {notifications_sent} donors"
        
    except BloodRequest.DoesNotExist:
        logger.error(f"Blood request {request_id} not found")
        return "Request not found"
    except Exception as e:
        logger.error(f"Error sending emergency notifications: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def send_email_notification(notification_id):
    """Send email notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        user = notification.user
        
        if not user.email:
            return "No email address"
        
        subject = notification.title
        message = notification.message
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        
        send_mail(subject, message, from_email, recipient_list)
        notification.email_sent = True
        notification.save()
        
        logger.info(f"Email sent to {user.email} for notification {notification_id}")
        return "Email sent successfully"
        
    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} not found")
        return "Notification not found"
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def send_sms_notification(notification_id):
    """Send SMS notification (placeholder - implement with SMS service)"""
    try:
        notification = Notification.objects.get(id=notification_id)
        user = notification.user
        
        # This is a placeholder - implement with actual SMS service
        # like Twilio, AWS SNS, or local SMS gateway
        phone_number = getattr(user, 'phone_number', None)
        if not phone_number:
            return "No phone number"
        
        # SMS sending logic would go here
        message = f"{notification.title}: {notification.message[:100]}..."
        
        # Simulate SMS sending
        logger.info(f"SMS would be sent to {phone_number}: {message}")
        notification.sms_sent = True
        notification.save()
        
        return "SMS sent successfully"
        
    except Notification.DoesNotExist:
        return "Notification not found"
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def send_donation_reminders():
    """Send reminders to donors who haven't donated in 3 months"""
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        # Find eligible donors (verified, available, not donated in 90 days)
        three_months_ago = timezone.now().date() - timedelta(days=90)
        eligible_donors = User.objects.filter(
            user_type='donor',
            is_verified=True,
            is_available=True,
            is_active=True,
            has_medical_conditions=False
        ).exclude(
            last_donation_date__gt=three_months_ago
        )
        
        reminders_sent = 0
        for donor in eligible_donors:
            # Check if they have notification preferences
            preferences = getattr(donor, 'notification_preferences', None)
            if preferences and not preferences.email_reminders:
                continue
            
            # Create reminder notification
            notification = Notification.objects.create(
                user=donor,
                notification_type='donation_reminder',
                priority='normal',
                title="Blood Donation Reminder",
                message=f"""Hello {donor.first_name or donor.username},
                
It's been over 3 months since your last blood donation. Your blood group {donor.blood_group} 
is always in demand to help save lives.

Consider donating blood at your nearest blood bank.

Thank you for your continued support!"""
            )
            
            # Send email
            if preferences is None or preferences.email_reminders:
                send_email_notification.delay(notification.id)
            
            reminders_sent += 1
        
        logger.info(f"Sent donation reminders to {reminders_sent} donors")
        return f"Reminders sent to {reminders_sent} donors"
        
    except Exception as e:
        logger.error(f"Error sending donation reminders: {str(e)}")
        return f"Error: {str(e)}"

@shared_task
def process_request_approval(request_id, approved_by_id, notes=""):
    """Process blood request approval workflow"""
    try:
        from accounts.models import User
        from requests.models import RequestUpdate
        
        blood_request = BloodRequest.objects.get(id=request_id)
        approved_by = User.objects.get(id=approved_by_id)
        
        # Update request status
        old_status = blood_request.status
        blood_request.status = 'approved'
        blood_request.approved_by = approved_by
        blood_request.approved_at = timezone.now()
        blood_request.approval_notes = notes
        blood_request.save()
        
        # Log status change
        RequestUpdate.objects.create(
            request=blood_request,
            updated_by=approved_by,
            status_from=old_status,
            status_to='approved',
            notes=notes
        )
        
        # Send notification to requester
        Notification.objects.create(
            user=blood_request.requester,
            notification_type='request_update',
            priority='normal',
            title="Blood Request Approved",
            message=f"Your blood request for {blood_request.patient_name} has been approved and is now active.",
            related_request=blood_request
        )
        
        logger.info(f"Request {request_id} approved by user {approved_by_id}")
        return "Request approved successfully"
        
    except Exception as e:
        logger.error(f"Error processing request approval: {str(e)}")
        return f"Error: {str(e)}"