from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.conf import settings
import time
import json

class RateLimitMiddleware(MiddlewareMixin):
    """Rate limiting middleware to prevent spam requests"""
    
    def process_request(self, request):
        # Skip rate limiting for admin and static files
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/')):
            return None
        
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Rate limit key
        cache_key = f"rate_limit_{ip}"
        
        # Get current count
        request_count = cache.get(cache_key, 0)
        
        # Check limits
        if request.user.is_authenticated:
            # Authenticated users: 1000 requests/hour
            limit = 1000
            time_window = 3600  # 1 hour
        else:
            # Anonymous users: 100 requests/hour
            limit = 100
            time_window = 3600  # 1 hour
        
        # Check if limit exceeded
        if request_count >= limit:
            return HttpResponseForbidden(
                json.dumps({'error': 'Rate limit exceeded'}),
                content_type='application/json'
            )
        
        # Increment count and set expiration
        cache.set(cache_key, request_count + 1, time_window)
        
        return None
    
    def get_client_ip(self, request):
        """Get real client IP (handle proxies/load balancers)"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class AuditMiddleware(MiddlewareMixin):
    """Audit logging middleware for data protection compliance"""
    
    def process_request(self, request):
        # Store request details for logging
        if not hasattr(request, '_audit_info'):
            request._audit_info = {}
        
        request._audit_info.update({
            'timestamp': time.time(),
            'method': request.method,
            'path': request.path,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        })
        
        return None
    
    def process_response(self, request, response):
        # Log the request/response
        if hasattr(request, '_audit_info'):
            # In production, send to logging system
            pass
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class PrivacyProtectionMiddleware(MiddlewareMixin):
    """Privacy protection middleware for GDPR compliance"""
    
    def process_response(self, request, response):
        # Add privacy headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Add data protection headers
        if settings.GDPR_COMPLIANCE_ENABLED:
            response['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'
        
        return response