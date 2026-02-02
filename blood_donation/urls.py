"""URL Configuration for blood_donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Public home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Frontend pages (no API prefix)
    path('accounts/', include('accounts.urls')),
    
    # Authentication API
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Core Apps APIs
    path('api/accounts/', include('accounts.urls')),
    path('api/donors/', include('donors.urls')),
    path('api/requests/', include('requests.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/analytics/', include('analytics.urls')),
]

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Blood Donation Platform Admin"
admin.site.site_title = "Blood Donation Admin Portal"
admin.site.index_title = "Welcome to Blood Donation Platform Administration"