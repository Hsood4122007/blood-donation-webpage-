from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'blood_group', 'city', 'is_verified', 'is_eligible_donor']
    list_filter = ['user_type', 'blood_group', 'is_verified', 'is_available', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'city']
    readonly_fields = ['created_at', 'updated_at', 'days_since_last_donation']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Blood Donation Info', {
            'fields': (
                'user_type', 'phone_number', 'blood_group', 'date_of_birth',
                'last_donation_date', 'days_since_last_donation', 'is_verified',
                'is_available', 'privacy_level'
            )
        }),
        ('Location', {
            'fields': ('city', 'state', 'country', 'pincode', 'latitude', 'longitude')
        }),
        ('Medical Info', {
            'fields': ('has_medical_conditions', 'medical_conditions', 'last_medical_checkup')
        }),
        ('GDPR Compliance', {
            'fields': ('consent_given', 'data_retention_consent', 'created_at', 'updated_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Blood Donation Info', {
            'fields': (
                'user_type', 'phone_number', 'blood_group', 'date_of_birth',
                'is_verified', 'privacy_level'
            )
        }),
    )