from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    days_since_last_donation = serializers.ReadOnlyField()
    is_eligible_donor = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'blood_group', 'date_of_birth',
            'last_donation_date', 'days_since_last_donation', 'is_eligible_donor',
            'is_verified', 'is_available', 'privacy_level',
            'city', 'state', 'country', 'pincode', 'latitude', 'longitude',
            'has_medical_conditions', 'medical_conditions', 'last_medical_checkup',
            'consent_given', 'data_retention_consent', 'password'
        ]
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'blood_group',
            'date_of_birth', 'is_available', 'privacy_level',
            'city', 'state', 'country', 'pincode', 'latitude', 'longitude',
            'has_medical_conditions', 'medical_conditions', 'last_medical_checkup'
        ]

class UserPublicSerializer(serializers.ModelSerializer):
    """Public serializer for user data (privacy-controlled)"""
    
    # Add distance field (will be added dynamically)
    distance_km = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'user_type', 'blood_group', 'city', 'state', 'pincode',
            'phone_number', 'distance_km'
        ]
    
    def get_distance_km(self, obj):
        # Return distance if available, otherwise None
        return getattr(obj, 'distance_km', None)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username
        token['user_type'] = user.user_type
        token['is_verified'] = user.is_verified
        token['blood_group'] = user.blood_group
        
        return token

class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification"""
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

