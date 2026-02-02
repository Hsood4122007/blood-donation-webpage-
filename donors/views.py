from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

from accounts.models import User
from accounts.serializers import UserPublicSerializer
from .matching import BloodMatcher

# Setup logging
logger = logging.getLogger(__name__)


class DonorSearchView(generics.ListAPIView):
    """
    Search for best-matching donors using the BloodMatcher.

    Query params:
    - blood_group (required)
    - latitude (required)
    - longitude (required)
    - max_distance (optional, default 25)
    - priority (optional: normal|urgent|emergency, default normal)
    - pincode (optional)
    - city (optional)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserPublicSerializer

    def list(self, request, *args, **kwargs):
        try:
            blood_group = request.query_params.get("blood_group")
            latitude = request.query_params.get("latitude")
            longitude = request.query_params.get("longitude")
            max_distance = request.query_params.get("max_distance", 25)
            priority = request.query_params.get("priority", "normal")
            pincode = request.query_params.get("pincode")
            city = request.query_params.get("city")

            if not all([blood_group, latitude, longitude]):
                logger.warning(f'Missing required parameters: blood_group={blood_group}, latitude={latitude}, longitude={longitude}')
                return Response(
                    {
                        "detail": "blood_group, latitude and longitude are required query parameters."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                latitude = float(latitude)
                longitude = float(longitude)
                max_distance = float(max_distance)
            except (TypeError, ValueError):
                logger.warning(f'Invalid numeric parameters: latitude={latitude}, longitude={longitude}, max_distance={max_distance}')
                return Response(
                    {"detail": "latitude, longitude and max_distance must be numbers."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get matches from BloodMatcher
            matches = BloodMatcher.get_best_matching_donors(
                blood_group=blood_group,
                latitude=latitude,
                longitude=longitude,
                priority=priority,
                limit=100,  # Increase limit to accommodate filtering
            )

            # Apply additional filters
            filtered_matches = []
            for match in matches:
                donor = match["donor"]
                
                # Filter by pincode if provided
                if pincode and donor.pincode != pincode:
                    continue
                    
                # Filter by city if provided
                if city and city.lower() not in donor.city.lower():
                    continue
                    
                donor_data = UserPublicSerializer(donor, context={"request": request}).data
                filtered_matches.append(
                    {
                        "donor": donor_data,
                        "score": match["score"],
                        "details": match["details"],
                    }
                )

            # Limit results to 50
            results = filtered_matches[:50]

            logger.info(f'Donor search completed: {len(results)} results for blood group {blood_group}')
            return Response({"count": len(results), "results": results})
            
        except Exception as e:
            logger.error(f'Error in donor search: {str(e)}', exc_info=True)
            return Response(
                {"detail": "An error occurred while searching for donors."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def compatibility_info(request, blood_group):
    """
    Return compatibility information for a given blood group.
    """
    try:
        info = BloodMatcher.get_compatibility_info(blood_group)
        logger.info(f'Compatibility info requested for blood group: {blood_group}')
        return Response(info)
    except Exception as e:
        logger.error(f'Error getting compatibility info for {blood_group}: {str(e)}', exc_info=True)
        return Response(
            {"detail": "An error occurred while fetching compatibility information."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


