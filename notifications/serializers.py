from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
from requests.serializers import BloodRequestSerializer
from .models import Notification


class NotificationRelatedRequestSerializer(BloodRequestSerializer):
    class Meta(BloodRequestSerializer.Meta):
        fields = [
            "id",
            "patient_name",
            "patient_blood_group",
            "hospital_name",
            "city",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    related_request = NotificationRelatedRequestSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_type",
            "priority",
            "title",
            "message",
            "user",
            "related_request",
            "is_read",
            "is_archived",
            "created_at",
        ]


