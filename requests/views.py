from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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


