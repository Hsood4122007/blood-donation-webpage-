# Blood Donation Platform

A comprehensive Django-based blood donation management system with advanced matching algorithms, real-time notifications, and analytics dashboard.

## 🏥 Project Overview

This blood donation platform connects patients in need of blood transfusions with eligible donors through an intelligent matching system. The platform includes hospital management, donor verification, emergency notifications, and comprehensive analytics.

## 🚀 Key Features

### Core Functionality
- **Smart Donor Matching**: Advanced algorithm matching donors by blood group, location, and availability
- **Emergency Notifications**: Real-time alerts to eligible donors via email and SMS
- **Request Management**: Hospital-based blood request system with approval workflow
- **Donor Management**: Comprehensive donor profiles with medical history tracking
- **Analytics Dashboard**: Real-time statistics and reporting

### Academic Features (For Project Evaluation)
✅ **JWT Authentication** - Secure token-based authentication  
✅ **Rate Limiting** - Anti-spam protection for API endpoints  
✅ **Audit Logging** - Comprehensive activity tracking for compliance  
✅ **Donor Privacy Controls** - GDPR-style privacy management  
✅ **Request Approval Workflow** - Multi-step verification process  
✅ **Automated Email Verification** - User account verification system  
✅ **CAPTCHA Protection** - Bot prevention for forms  
✅ **GDPR-style Data Protection** - Privacy by design architecture  

## 🏗️ System Architecture

```
blood_donation/
├── accounts/          # User management and authentication
├── donors/           # Donor profiles and matching algorithms
├── requests/         # Blood request management
├── notifications/    # Notification system and templates
├── analytics/        # Dashboard and reporting
├── blood_donation/   # Main project configuration
└── apps/core/        # Shared utilities and middleware
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: MySQL 8.0 (optimized schema)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Task Queue**: Celery with Redis
- **Caching**: Redis
- **Security**: Rate limiting, audit logging, privacy controls
- **Monitoring**: Django Admin + Custom Analytics

## 📊 Database Schema

### Key Tables
- `accounts_user` - Extended user model with donor/hospital profiles
- `donors_donorhistory` - Donation history tracking
- `requests_bloodrequest` - Blood request management
- `notifications_notification` - User notification system
- `analytics_metrics` - System metrics and statistics

### Optimizations
- Spatial indexing for location-based queries
- Composite indexes for frequent query patterns
- Foreign key constraints for data integrity
- Audit trails for compliance

## 🔍 Matching Algorithm

The platform implements a sophisticated blood donor matching algorithm:

### Compatibility Matrix
```
A+  ↔  A+, A-, O+, O-
A-  ↔  A-, O-
B+  ↔  B+, B-, O+, O-
B-  ↔  B-, O-
AB+ ↔  All blood groups (Universal recipient)
AB- ↔  A-, B-, AB-, O-
O+  ↔  O+, O-
O-  ↔  O- (Universal donor)
```

### Scoring System
1. **Distance Score** (0-30 points): Based on proximity to request location
2. **History Score** (0-25 points): Based on donation frequency and reliability
3. **Reliability Score** (0-20 points): Based on donor ratings and feedback
4. **Urgency Multiplier** (1.0-1.5x): Priority-based boosting

## 📱 API Endpoints

### Authentication
```
POST /api/auth/token/          # Get JWT token
POST /api/auth/token/refresh/  # Refresh token
POST /api/accounts/register/   # User registration
```

### Donor Management
```
GET /api/donors/search/        # Find matching donors
GET /api/donors/profile/       # Donor profile
PUT /api/donors/profile/       # Update profile
```

### Blood Requests
```
POST /api/requests/create/     # Create blood request
GET /api/requests/list/        # List requests
GET /api/requests/{id}/        # Request details
```

### Notifications
```
GET /api/notifications/        # User notifications
POST /api/notifications/read/  # Mark as read
```

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Redis 6.0+

### Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd blood-donation-platform

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Start services
redis-server  # In separate terminal
celery -A blood_donation worker -l info  # In separate terminal
python manage.py runserver
```

## 🚨 Emergency Workflow

1. **Request Creation**: Hospital creates urgent blood request
2. **Approval**: Admin approves request (workflow system)
3. **Matching**: Algorithm finds eligible donors within 25km radius
4. **Notification**: Automated emails/SMS sent to matching donors
5. **Response**: Donors accept/decline requests
6. **Coordination**: System facilitates donation scheduling
7. **Completion**: Donation recorded and request updated

## 📈 Analytics Dashboard

The admin dashboard provides:
- Real-time donor statistics
- Request fulfillment rates
- Geographic distribution maps
- Monthly donation trends
- Emergency response times
- System performance metrics

## 🔒 Security Features

### Authentication & Authorization
- JWT token authentication
- Role-based access control
- Session management
- Password strength validation

### Data Protection
- GDPR compliance features
- Data encryption at rest
- Privacy controls for users
- Audit logging for all actions
- Data retention policies

### API Security
- Rate limiting (100/hr anonymous, 1000/hr authenticated)
- Input validation and sanitization
- CORS protection
- Security headers
- Request/response logging

## 🎯 Academic Excellence Features

This project demonstrates advanced software engineering concepts:

### Software Architecture
- **Modular Design**: Separated apps for different concerns
- **SOLID Principles**: Well-structured, maintainable code
- **Design Patterns**: Observer, Factory, Strategy patterns
- **API First**: RESTful design with proper versioning

### Advanced Features
- **Background Processing**: Celery for async tasks
- **Real-time Notifications**: Email and SMS integration
- **Geospatial Queries**: Location-based matching
- **Scalable Architecture**: Designed for high availability

### Best Practices
- **Code Quality**: PEP 8 compliance, comprehensive documentation
- **Testing**: Unit tests, integration tests planned
- **CI/CD**: Deployment automation ready
- **Monitoring**: Comprehensive logging and metrics

### Compliance & Standards
- **GDPR Ready**: Privacy by design implementation
- **Medical Standards**: HIPAA-inspired data handling
- **Accessibility**: WCAG compliance considerations
- **Internationalization**: Multi-language support ready

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Render Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md)
- [Security Manual](docs/security.md)
- [User Guide](docs/user_guide.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is for educational purposes. All rights reserved.

## 🎓 Academic Value

This project demonstrates:
- **Full-stack Development**: Backend, database, and system design
- **Real-world Problem Solving**: Addressing critical healthcare needs
- **Advanced Algorithms**: Geospatial matching and optimization
- **Enterprise Features**: Security, compliance, scalability
- **Professional Standards**: Documentation, testing, deployment

Perfect for computer science and software engineering students seeking to demonstrate advanced development skills and understanding of complex system design.

---
*Built with ❤️ for saving lives through technology*#   F o r c e   r e d e p l o y  
 