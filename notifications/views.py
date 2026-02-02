from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import logging

from .models import Notification
from .serializers import NotificationSerializer

# Setup logging
logger = logging.getLogger(__name__)


class NotificationListView(generics.ListAPIView):
    """
    List notifications for the authenticated user.
    Supports filtering by is_read.
    """

    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = Notification.objects.filter(user=self.request.user)
            is_read = self.request.query_params.get("is_read")
            if is_read is not None:
                if is_read.lower() == "true":
                    queryset = queryset.filter(is_read=True)
                elif is_read.lower() == "false":
                    queryset = queryset.filter(is_read=False)
            logger.info(f'Notifications list requested for user: {self.request.user.id}')
            return queryset
        except Exception as e:
            logger.error(f'Error getting notifications for user {self.request.user.id}: {str(e)}', exc_info=True)
            raise


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """
    Mark a notification as read.
    """
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.mark_as_read()
        logger.info(f'Notification {pk} marked as read for user: {request.user.id}')
        return Response({"message": "Notification marked as read"})
    except Notification.DoesNotExist:
        logger.warning(f'Notification {pk} not found for user: {request.user.id}')
        return Response(
            {"detail": "Notification not found."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(f'Error marking notification {pk} as read: {str(e)}', exc_info=True)
        return Response(
            {"detail": "An error occurred while marking notification as read."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


