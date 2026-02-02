from datetime import timedelta

from django.utils import timezone
from django.db.models import Count, Avg
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from accounts.models import User
from donors.models import DonorHistory
from requests.models import BloodRequest

# Setup logging
logger = logging.getLogger(__name__)


class SystemStatsView(APIView):
    """
    Return high-level system statistics for the dashboard.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            total_donors = User.objects.filter(user_type="donor").count()
            active_donors = User.objects.filter(
                user_type="donor", is_active=True, is_available=True
            ).count()
            verified_donors = User.objects.filter(
                user_type="donor", is_active=True, is_verified=True
            ).count()

            total_requests = BloodRequest.objects.count()
            active_requests = BloodRequest.objects.filter(
                status__in=["approved", "active", "partially_fulfilled"]
            ).count()
            fulfilled_requests = BloodRequest.objects.filter(status="fulfilled").count()

            total_donations = DonorHistory.objects.count()

            # Placeholder for average response time; requires additional tracking in real app
            average_response_time_hours = 0

            data = {
                "total_donors": total_donors,
                "active_donors": active_donors,
                "verified_donors": verified_donors,
                "total_requests": total_requests,
                "active_requests": active_requests,
                "fulfilled_requests": fulfilled_requests,
                "total_donations": total_donations,
                "successful_matches": 0,
                "average_response_time_hours": average_response_time_hours,
            }
            logger.info('System stats requested successfully')
            return Response(data)
        except Exception as e:
            logger.error(f'Error getting system stats: {str(e)}', exc_info=True)
            return Response(
                {"detail": "An error occurred while fetching system statistics."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DonorDistributionView(APIView):
    """
    Distribution of donors by blood group and city.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            donors_qs = User.objects.filter(user_type="donor")

            by_blood_group = (
                donors_qs.values_list("blood_group")
                .exclude(blood_group__isnull=True)
                .annotate(count=Count("id"))
            )
            blood_group_data = {bg or "Unknown": c for bg, c in by_blood_group}

            by_city = (
                donors_qs.values_list("city")
                .exclude(city__exact="")
                .annotate(count=Count("id"))
            )
            city_data = {city or "Unknown": c for city, c in by_city}

            logger.info('Donor distribution requested successfully')
            return Response({"by_blood_group": blood_group_data, "by_city": city_data})
        except Exception as e:
            logger.error(f'Error getting donor distribution: {str(e)}', exc_info=True)
            return Response(
                {"detail": "An error occurred while fetching donor distribution."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MonthlyTrendsView(APIView):
    """
    Simple monthly trends for donations and requests.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            months = int(request.query_params.get("months", 6))
            end_date = timezone.now().date().replace(day=1)
            start_date = end_date - timedelta(days=months * 31)

            donations = (
                DonorHistory.objects.filter(donation_date__date__gte=start_date)
                .extra(select={"month": "DATE_FORMAT(donation_date, '%%Y-%%m')"})
                .values("month")
                .annotate(count=Count("id"))
                .order_by("month")
            )

            requests = (
                BloodRequest.objects.filter(created_at__date__gte=start_date)
                .extra(select={"month": "DATE_FORMAT(created_at, '%%Y-%%m')"})
                .values("month")
                .annotate(count=Count("id"))
                .order_by("month")
            )

            logger.info(f'Monthly trends requested for {months} months')
            return Response(
                {
                    "donations": list(donations),
                    "requests": list(requests),
                }
            )
        except Exception as e:
            logger.error(f'Error getting monthly trends: {str(e)}', exc_info=True)
            return Response(
                {"detail": "An error occurred while fetching monthly trends."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


