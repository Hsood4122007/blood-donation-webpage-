# Blood Donation Platform - API Documentation

## Authentication Endpoints

### Get JWT Token
```
POST /api/auth/token/
Content-Type: application/json

{
    "username": "donor1",
    "password": "donor123"
}

Response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token
```
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Management

### Register New User
```
POST /api/accounts/register/
Content-Type: application/json

{
    "username": "newdonor",
    "email": "newdonor@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "donor",
    "phone_number": "+919876543210",
    "blood_group": "O+",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "consent_given": true,
    "data_retention_consent": true
}
```

### Get User Profile
```
GET /api/accounts/profile/
Authorization: Bearer <access_token>

Response:
{
    "id": 1,
    "username": "donor1",
    "email": "donor1@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "donor",
    "phone_number": "+919876543210",
    "blood_group": "O+",
    "date_of_birth": "1990-01-01",
    "last_donation_date": "2024-01-15",
    "days_since_last_donation": 45,
    "is_eligible_donor": true,
    "is_verified": true,
    "is_available": true,
    "privacy_level": "public",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India"
}
```

### Update Profile
```
PUT /api/accounts/profile/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Smith",
    "phone_number": "+919876543211",
    "is_available": true
}
```

## Donor Search and Matching

### Search Matching Donors
```
GET /api/donors/search/?blood_group=O+&latitude=19.0760&longitude=72.8777&max_distance=25
Authorization: Bearer <access_token>

Response:
{
    "count": 15,
    "results": [
        {
            "donor": {
                "id": 1,
                "username": "donor1",
                "first_name": "John",
                "last_name": "Doe",
                "blood_group": "O+",
                "city": "Mumbai",
                "state": "Maharashtra"
            },
            "score": 87.5,
            "details": {
                "distance_km": 2.5,
                "distance_score": 30,
                "history_score": 25,
                "reliability_score": 20,
                "urgency_multiplier": 1.2
            }
        }
    ]
}
```

### Get Donor Compatibility Info
```
GET /api/donors/compatibility/O+/
Authorization: Bearer <access_token>

Response:
{
    "required_blood_group": "O+",
    "compatible_donors": ["O+", "O-"],
    "is_universal_recipient": false,
    "is_universal_donor": false,
    "total_compatible_types": 2
}
```

## Blood Request Management

### Create Blood Request
```
POST /api/requests/create/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient_name": "Patient Name",
    "patient_age": 35,
    "patient_blood_group": "AB-",
    "required_units": 2,
    "priority": "emergency",
    "reason": "Car accident requiring immediate blood transfusion",
    "required_by": "2024-02-05T10:00:00Z",
    "hospital_name": "City Hospital",
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "contact_person": "Dr. Smith",
    "contact_phone": "+919876543210",
    "contact_email": "dr.smith@hospital.com"
}
```

### List Blood Requests
```
GET /api/requests/list/?status=active&priority=emergency
Authorization: Bearer <access_token>

Response:
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "patient_name": "Patient Name",
            "patient_blood_group": "AB-",
            "required_units": 2,
            "fulfilled_units": 0,
            "priority": "emergency",
            "status": "active",
            "hospital_name": "City Hospital",
            "city": "Mumbai",
            "required_by": "2024-02-05T10:00:00Z",
            "created_at": "2024-02-02T15:30:00Z"
        }
    ]
}
```

### Get Request Details
```
GET /api/requests/1/
Authorization: Bearer <access_token>

Response:
{
    "id": 1,
    "requester": {
        "id": 5,
        "username": "hospital1",
        "first_name": "City Hospital Mumbai"
    },
    "patient_name": "Patient Name",
    "patient_age": 35,
    "patient_blood_group": "AB-",
    "required_units": 2,
    "fulfilled_units": 0,
    "remaining_units": 2,
    "completion_percentage": 0,
    "priority": "emergency",
    "status": "active",
    "reason": "Car accident requiring immediate blood transfusion",
    "required_by": "2024-02-05T10:00:00Z",
    "hospital_name": "City Hospital",
    "city": "Mumbai",
    "contact_person": "Dr. Smith",
    "contact_phone": "+919876543210",
    "contact_email": "dr.smith@hospital.com",
    "matches": [
        {
            "id": 1,
            "donor": {
                "id": 1,
                "username": "donor1",
                "first_name": "John",
                "last_name": "Doe",
                "blood_group": "AB-"
            },
            "status": "proposed",
            "distance_km": 2.5,
            "compatibility_score": 87.5,
            "proposed_at": "2024-02-02T16:00:00Z"
        }
    ]
}
```

## Notifications

### List User Notifications
```
GET /api/notifications/?is_read=false
Authorization: Bearer <access_token>

Response:
{
    "count": 3,
    "results": [
        {
            "id": 1,
            "notification_type": "request_match",
            "priority": "urgent",
            "title": "Emergency Blood Request - AB-",
            "message": "Urgent blood donation needed for Patient Name...",
            "is_read": false,
            "created_at": "2024-02-02T16:15:00Z",
            "related_request": {
                "id": 1,
                "patient_name": "Patient Name",
                "patient_blood_group": "AB-"
            }
        }
    ]
}
```

### Mark Notification as Read
```
POST /api/notifications/1/read/
Authorization: Bearer <access_token>

Response:
{
    "message": "Notification marked as read"
}
```

## Analytics Endpoints

### System Statistics
```
GET /api/analytics/stats/
Authorization: Bearer <access_token>

Response:
{
    "total_donors": 1250,
    "active_donors": 847,
    "verified_donors": 1123,
    "total_requests": 156,
    "active_requests": 23,
    "fulfilled_requests": 133,
    "total_donations": 892,
    "successful_matches": 234,
    "average_response_time_hours": 2.5
}
```

### Donor Distribution
```
GET /api/analytics/donor-distribution/
Authorization: Bearer <access_token>

Response:
{
    "by_blood_group": {
        "A+": 320,
        "A-": 45,
        "B+": 280,
        "B-": 38,
        "AB+": 89,
        "AB-": 22,
        "O+": 345,
        "O-": 51
    },
    "by_city": {
        "Mumbai": 425,
        "Delhi": 280,
        "Bangalore": 195,
        "Hyderabad": 156,
        "Chennai": 194
    }
}
```

### Monthly Trends
```
GET /api/analytics/monthly-trends/?months=6
Authorization: Bearer <access_token>

Response:
{
    "donations": [
        {"month": "2023-09", "count": 142},
        {"month": "2023-10", "count": 156},
        {"month": "2023-11", "count": 168},
        {"month": "2023-12", "count": 134},
        {"month": "2024-01", "count": 178},
        {"month": "2024-02", "count": 45}
    ],
    "requests": [
        {"month": "2023-09", "count": 22},
        {"month": "2023-10", "count": 18},
        {"month": "2023-11", "count": 25},
        {"month": "2023-12", "count": 15},
        {"month": "2024-01", "count": 28},
        {"month": "2024-02", "count": 8}
    ]
}
```

## Error Responses

### Validation Error
```
Status: 400 Bad Request
{
    "email": ["Enter a valid email address."],
    "password": ["This password is too common."]
}
```

### Authentication Error
```
Status: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```
Status: 403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}
```

### Not Found
```
Status: 404 Not Found
{
    "detail": "Not found."
}
```

## Rate Limiting

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Response when rate limited**: 429 Too Many Requests

```json
{
    "error": "Rate limit exceeded"
}
```

## Pagination

All list endpoints support pagination:
```
GET /api/requests/list/?page=2&page_size=10
```

Response includes:
```json
{
    "count": 45,
    "next": "http://api.example.com/requests/?page=3",
    "previous": "http://api.example.com/requests/?page=1",
    "results": [...]
}
```

This API provides a complete interface for building blood donation platform applications with proper authentication, authorization, and rate limiting.