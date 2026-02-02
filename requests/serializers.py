from rest_framework import serializers

from accounts.serializers import UserPublicSerializer
from .models import BloodRequest, RequestMatch


class BloodRequestSerializer(serializers.ModelSerializer):
    requester = UserPublicSerializer(read_only=True)

    remaining_units = serializers.ReadOnlyField()
    completion_percentage = serializers.ReadOnlyField()

    class Meta:
        model = BloodRequest
        fields = [
            "id",
            "requester",
            "patient_name",
            "patient_age",
            "patient_blood_group",
            "required_units",
            "fulfilled_units",
            "remaining_units",
            "completion_percentage",
            "priority",
            "status",
            "requester_type",
            "reason",
            "required_by",
            "medical_certificate",
            "is_critical",
            "hospital_name",
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "contact_person",
            "contact_phone",
            "contact_email",
            "approved_by",
            "approved_at",
            "approval_notes",
            "created_at",
            "updated_at",
            "expires_at",
        ]
        read_only_fields = [
            "id",
            "requester",
            "fulfilled_units",
            "remaining_units",
            "completion_percentage",
            "approved_by",
            "approved_at",
            "created_at",
            "updated_at",
            "expires_at",
        ]


class BloodRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodRequest
        fields = [
            "patient_name",
            "patient_age",
            "patient_blood_group",
            "required_units",
            "priority",
            "requester_type",
            "reason",
            "required_by",
            "medical_certificate",
            "is_critical",
            "hospital_name",
            "city",
            "state",
            "country",
            "latitude",
            "longitude",
            "contact_person",
            "contact_phone",
            "contact_email",
        ]


class RequestMatchDonorSerializer(UserPublicSerializer):
    class Meta(UserPublicSerializer.Meta):
        fields = UserPublicSerializer.Meta.fields + ["blood_group"]


class RequestMatchSerializer(serializers.ModelSerializer):
    donor = RequestMatchDonorSerializer(read_only=True)

    class Meta:
        model = RequestMatch
        fields = [
            "id",
            "donor",
            "status",
            "proposed_at",
            "responded_at",
            "donation_scheduled_at",
            "donation_completed_at",
            "notes",
            "distance_km",
            "compatibility_score",
        ]


class BloodRequestDetailSerializer(BloodRequestSerializer):
    matches = RequestMatchSerializer(many=True, read_only=True)

    class Meta(BloodRequestSerializer.Meta):
        fields = BloodRequestSerializer.Meta.fields + ["matches"]


