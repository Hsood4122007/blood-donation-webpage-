from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import logging

from .models import BloodRequest
from .serializers import (
    BloodRequestSerializer,
    BloodRequestCreateSerializer,
    BloodRequestDetailSerializer,
)

# Setup logging
logger = logging.getLogger(__name__)


class BloodRequestCreateView(generics.CreateAPIView):
    """
    Create a new blood request.
    """

    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(requester=self.request.user)
            logger.info(f'Blood request created by user: {self.request.user.id}')
        except Exception as e:
            logger.error(f'Error creating blood request: {str(e)}', exc_info=True)
            raise


class BloodRequestListView(generics.ListAPIView):
    """
    List blood requests with basic filtering.
    """

    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "city", "patient_blood_group"]
    ordering_fields = ["created_at", "required_by", "priority"]
    ordering = ["-created_at"]


class BloodRequestDetailView(generics.RetrieveAPIView):
    """
    Retrieve full details of a blood request, including matches.
    """

    queryset = BloodRequest.objects.all()
    serializer_class = BloodRequestDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([AllowAny])
def live_blood_requests(request):
    """
    API endpoint to fetch live/active blood requests for homepage display.
    Returns recent active requests ordered by urgency and creation time.
    """
    try:
        # Get active, non-expired requests
        now = timezone.now()
        live_requests = BloodRequest.objects.filter(
            status__in=['active', 'approved'],
            expires_at__gt=now,
            required_by__gte=now
        ).order_by(
            # Priority ordering: emergency > urgent > normal
            '-priority',
            '-created_at'
        )[:10]  # Limit to 10 most recent
        
        # Serialize data manually for custom format
        data = []
        for req in live_requests:
            data.append({
                'id': req.id,
                'blood_group': req.patient_blood_group,
                'location': f"{req.city}, {req.state}",
                'urgency': req.priority,
                'urgency_display': req.get_priority_display(),
                'hospital': req.hospital_name,
                'required_units': req.required_units,
                'fulfilled_units': req.fulfilled_units,
                'remaining_units': req.remaining_units,
                'contact_phone': req.contact_phone,
                'created_at': req.created_at.isoformat(),
                'time_ago': get_time_ago(req.created_at),
                'is_critical': req.is_critical,
            })
        
        logger.info(f'Live blood requests fetched: {len(data)} active requests')
        return Response(data)
        
    except Exception as e:
        logger.error(f'Error fetching live blood requests: {str(e)}', exc_info=True)
        return Response(
            {'detail': 'An error occurred while fetching live blood requests.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def get_time_ago(dt):
    """
    Helper function to convert datetime to human-readable time ago format.
    """
    now = timezone.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'Just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        weeks = int(seconds / 604800)
        return f'{weeks} week{"s" if weeks > 1 else ""} ago'


# Add compatibility alias for older code
live_requests_view = live_blood_requests


