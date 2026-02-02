import math
from django.db.models import Q
from django.utils import timezone
from accounts.models import User
from .models import DonorAvailability
from datetime import timedelta

class BloodMatcher:
    """Core blood donor matching algorithm"""
    
    # Blood compatibility matrix
    COMPATIBILITY_MATRIX = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'A-': ['A-', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'B-': ['B-', 'O-'],
        'AB+': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],  # Universal recipient
        'AB-': ['A-', 'B-', 'AB-', 'O-'],
        'O+': ['O+', 'O-'],
        'O-': ['O-']  # Universal donor
    }
    
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate distance between two points using Haversine formula
        Returns distance in kilometers
        """
        if not all([lat1, lon1, lat2, lon2]):
            return float('inf')
            
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    @classmethod
    def find_matching_donors(cls, blood_group, latitude, longitude, max_distance_km=25, 
                           include_unavailable=False):
        """
        Find eligible donors within specified radius
        
        Args:
            blood_group (str): Required blood group
            latitude (float): Request location latitude
            longitude (float): Request location longitude
            max_distance_km (int): Maximum distance in kilometers
            include_unavailable (bool): Include unavailable donors
        
        Returns:
            QuerySet of matching donors with distance annotation
        """
        # Get compatible blood groups
        compatible_blood_groups = cls.COMPATIBILITY_MATRIX.get(blood_group, [])
        
        # Build base query for eligible donors
        query = Q(
            user_type='donor',
            blood_group__in=compatible_blood_groups,
            is_verified=True,
            is_active=True
        )
        
        # Add availability filter if not including unavailable donors
        if not include_unavailable:
            query &= Q(is_available=True)
            # Also check availability model
            available_donors = DonorAvailability.objects.filter(
                is_available=True
            ).values_list('donor_id', flat=True)
            query &= Q(id__in=available_donors)
        
        # Filter donors by medical eligibility
        query &= Q(has_medical_conditions=False)
        
        # Filter by donation frequency (minimum 90 days since last donation)
        min_donation_date = timezone.now().date() - timedelta(days=90)
        query &= (
            Q(last_donation_date__isnull=True) | 
            Q(last_donation_date__lte=min_donation_date)
        )
        
        # Get donors
        donors = User.objects.filter(query)
        
        # Calculate distances and filter by radius
        matching_donors = []
        for donor in donors:
            distance = cls.calculate_distance(
                latitude, longitude,
                float(donor.latitude) if donor.latitude else None,
                float(donor.longitude) if donor.longitude else None
            )
            
            if distance <= max_distance_km:
                donor.distance_km = round(distance, 2)
                matching_donors.append(donor)
        
        # Sort by distance
        matching_donors.sort(key=lambda x: x.distance_km)
        
        return matching_donors
    
    @classmethod
    def get_donor_score(cls, donor, request_priority='normal'):
        """
        Calculate donor matching score based on multiple factors
        
        Args:
            donor: User instance
            request_priority: 'normal', 'urgent', 'emergency'
        
        Returns:
            dict with score details
        """
        score = 0
        details = {}
        
        # Distance score (0-30 points)
        if hasattr(donor, 'distance_km'):
            if donor.distance_km <= 5:
                distance_score = 30
            elif donor.distance_km <= 10:
                distance_score = 25
            elif donor.distance_km <= 15:
                distance_score = 20
            elif donor.distance_km <= 20:
                distance_score = 15
            else:
                distance_score = 10
            score += distance_score
            details['distance_score'] = distance_score
        
        # Donation history score (0-25 points)
        donation_count = donor.donation_history.count()
        if donation_count >= 10:
            history_score = 25
        elif donation_count >= 5:
            history_score = 20
        elif donation_count >= 2:
            history_score = 15
        elif donation_count >= 1:
            history_score = 10
        else:
            history_score = 5
        score += history_score
        details['history_score'] = history_score
        
        # Availability reliability score (0-20 points)
        ratings = donor.ratings.all()
        if ratings.exists():
            avg_rating = sum(r.rating for r in ratings) / len(ratings)
            reliability_score = int(avg_rating * 4)  # 1-5 rating to 4-20 points
        else:
            reliability_score = 10  # Default for new donors
        score += reliability_score
        details['reliability_score'] = reliability_score
        
        # Urgency multiplier
        if request_priority == 'emergency':
            score *= 1.5
            details['urgency_multiplier'] = 1.5
        elif request_priority == 'urgent':
            score *= 1.2
            details['urgency_multiplier'] = 1.2
        else:
            details['urgency_multiplier'] = 1.0
        
        details['total_score'] = round(score, 2)
        return details
    
    @classmethod
    def get_best_matching_donors(cls, blood_group, latitude, longitude, 
                               priority='normal', limit=20):
        """
        Get best matching donors sorted by comprehensive score
        
        Args:
            blood_group (str): Required blood group
            latitude (float): Request location latitude
            longitude (float): Request location longitude
            priority (str): Request priority level
            limit (int): Maximum number of donors to return
        
        Returns:
            List of donors with scores, sorted by best match
        """
        # Get matching donors
        donors = cls.find_matching_donors(blood_group, latitude, longitude)
        
        # Calculate scores for each donor
        donors_with_scores = []
        for donor in donors:
            score_details = cls.get_donor_score(donor, priority)
            donors_with_scores.append({
                'donor': donor,
                'score': score_details['total_score'],
                'details': score_details
            })
        
        # Sort by score (descending)
        donors_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Return top matches
        return donors_with_scores[:limit]
    
    @classmethod
    def get_compatibility_info(cls, blood_group):
        """
        Get detailed compatibility information for a blood group
        
        Returns:
            dict with compatibility details
        """
        compatible_donors = cls.COMPATIBILITY_MATRIX.get(blood_group, [])
        return {
            'required_blood_group': blood_group,
            'compatible_donors': compatible_donors,
            'is_universal_recipient': blood_group == 'AB+',
            'is_universal_donor': blood_group == 'O-',
            'total_compatible_types': len(compatible_donors)
        }