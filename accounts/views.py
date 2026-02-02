from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .serializers import (
    UserSerializer, UserUpdateSerializer, UserPublicSerializer,
    CustomTokenObtainPairSerializer, EmailVerificationSerializer
)
from .models import User
import random
import string
import logging

# Setup logging
logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view"""
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Send verification email (in production, use Celery)
        send_verification_email(user)
    
    def create(self, request, *args, **kwargs):
        # Override create to customize response
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Return success response with user data
        return Response(
            {
                'message': 'User registered successfully',
                'user': serializer.data
            }, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile endpoint"""
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class PublicProfileView(generics.RetrieveAPIView):
    """Public user profile view (privacy-controlled)"""
    queryset = User.objects.filter(privacy_level='public')
    serializer_class = UserPublicSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    """Email verification endpoint"""
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        code = serializer.validated_data['verification_code']
        
        try:
            user = User.objects.get(email=email)
            # In production, verify against stored code
            if verify_code(user, code):
                user.is_verified = True
                user.save()
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# Helper functions (implement properly in production)
def send_verification_email(user):
    """Send email verification"""
    code = ''.join(random.choices(string.digits, k=6))
    # Store code in cache with expiration
    subject = 'Verify your email - Blood Donation Platform'
    message = f'Your verification code is: {code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def verify_code(user, code):
    """Verify email code"""
    # Check against stored code
    return True  # Simplified for example



def donor_registration_view(request):
    """Render the donor registration page with blood types"""
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    return render(request, 'accounts/register_donor.html', {'blood_types': blood_types})



def login_view(request):
    """Handle login page rendering and authentication"""
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('/accounts/dashboard/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter both username/email and password.')
            return render(request, 'accounts/login.html')
        
        # Handle both username and email login
        # Try authenticating with username first
        user = authenticate(request, username=username, password=password)
        
        # If that fails, try with email
        if user is None:
            User = get_user_model()
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                # Redirect to dashboard or home page
                next_url = request.GET.get('next', '/accounts/dashboard/')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid username/email or password. Please try again.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('/')


def donor_search_page(request):
    """Render the donor search page (only for authenticated users)"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access the search feature.')
        return redirect('/accounts/login/')
    
    return render(request, 'search/donor_search.html')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """API endpoint to update user profile"""
    user = request.user
    
    # Fields that can be updated
    updatable_fields = [
        'first_name', 'last_name', 'phone_number', 
        'blood_group', 'date_of_birth', 'city', 
        'state', 'country', 'pincode', 'is_available'
    ]
    
    # Update fields
    for field in updatable_fields:
        if field in request.data:
            value = request.data[field]
            # Handle boolean conversion for is_available field
            if field == 'is_available':
                if isinstance(value, str):
                    # Convert string boolean to actual boolean
                    value = value.lower() in ['true', '1', 'yes', 'on']
                elif isinstance(value, bool):
                    # Already boolean, keep as is
                    pass
                else:
                    # Convert other types to boolean
                    value = bool(value)
            
            setattr(user, field, value)
    
    try:
        user.save()
        serializer = UserPublicSerializer(user)
        return Response({
            'message': 'Profile updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f'Profile update error: {str(e)}', exc_info=True)
        
        # Return user-friendly error message
        error_msg = str(e)
        if 'true" value must be either True or False' in error_msg:
            error_msg = 'Invalid availability status. Please select "Available for donation" or "Not available".'
        
        return Response({
            'error': f'Failed to update profile: {error_msg}'
        }, status=status.HTTP_400_BAD_REQUEST)

def profile_page(request):
    """Render user profile page"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to view your profile.')
        return redirect('/accounts/login/')
    
    return render(request, 'accounts/profile.html', {'user': request.user})


def dashboard_page(request):
    """Render user dashboard page"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to access your dashboard.')
        return redirect('/accounts/login/')
    
    # Get user statistics
    stats = {
        'is_eligible': request.user.is_eligible_donor,
        'days_since_donation': request.user.days_since_last_donation,
        'can_donate': request.user.is_eligible_donor and request.user.is_available
    }
    
    return render(request, 'accounts/dashboard.html', {'user': request.user, 'stats': stats})

