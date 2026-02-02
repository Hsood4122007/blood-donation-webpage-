# Blood Donation Platform - Database Schema Documentation

## Overview

This document describes the database schema for the Blood Donation Platform, designed for optimal performance and data integrity.

## Core Tables

### 1. accounts_user
**Extended Django User Model**

```sql
CREATE TABLE accounts_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254),
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined DATETIME NOT NULL,
    user_type ENUM('donor', 'hospital', 'admin') DEFAULT 'donor',
    phone_number VARCHAR(15),
    blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
    date_of_birth DATE,
    last_donation_date DATE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    privacy_level ENUM('public', 'private') DEFAULT 'public',
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    has_medical_conditions BOOLEAN DEFAULT FALSE,
    medical_conditions TEXT,
    last_medical_checkup DATE,
    consent_given BOOLEAN DEFAULT FALSE,
    data_retention_consent BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_type (user_type),
    INDEX idx_blood_group (blood_group),
    INDEX idx_location (latitude, longitude),
    INDEX idx_verification (is_verified, is_active),
    SPATIAL INDEX idx_geo_location (latitude, longitude)
);
```

### 2. donors_donorhistory
**Donation History Tracking**

```sql
CREATE TABLE donors_donorhistory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    donor_id BIGINT NOT NULL,
    donation_type ENUM('whole_blood', 'plasma', 'platelets') DEFAULT 'whole_blood',
    donation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    hospital VARCHAR(200),
    city VARCHAR(100),
    blood_group VARCHAR(3),
    volume_ml INT DEFAULT 450,
    hemoglobin_level DECIMAL(4,2),
    notes TEXT,
    is_successful BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (donor_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    INDEX idx_donor_date (donor_id, donation_date),
    INDEX idx_blood_group (blood_group),
    INDEX idx_city (city)
);
```

### 3. requests_bloodrequest
**Blood Request Management**

```sql
CREATE TABLE requests_bloodrequest (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    requester_id BIGINT NOT NULL,
    patient_name VARCHAR(200) NOT NULL,
    patient_age INT NOT NULL,
    patient_blood_group ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    required_units INT DEFAULT 1,
    fulfilled_units INT DEFAULT 0,
    priority ENUM('normal', 'urgent', 'emergency') DEFAULT 'normal',
    status ENUM('pending', 'approved', 'active', 'partially_fulfilled', 'fulfilled', 'cancelled', 'expired') DEFAULT 'pending',
    requester_type ENUM('hospital', 'individual', 'relative') DEFAULT 'hospital',
    reason TEXT NOT NULL,
    required_by DATETIME NOT NULL,
    medical_certificate VARCHAR(100),
    is_critical BOOLEAN DEFAULT FALSE,
    hospital_name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) DEFAULT 'India',
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(15) NOT NULL,
    contact_email VARCHAR(254) NOT NULL,
    approved_by_id BIGINT,
    approved_at DATETIME,
    approval_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    expires_at DATETIME NOT NULL,
    
    FOREIGN KEY (requester_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by_id) REFERENCES accounts_user(id) ON DELETE SET NULL,
    INDEX idx_status_priority (status, priority),
    INDEX idx_location_blood (city, patient_blood_group),
    INDEX idx_expires_at (expires_at),
    SPATIAL INDEX idx_request_location (latitude, longitude)
);
```

### 4. notifications_notification
**User Notification System**

```sql
CREATE TABLE notifications_notification (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    notification_type ENUM('request_match', 'request_update', 'donation_reminder', 'system_alert', 'verification', 'admin_message') NOT NULL,
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    related_request_id BIGINT,
    is_read BOOLEAN DEFAULT FALSE,
    is_archived BOOLEAN DEFAULT FALSE,
    read_at DATETIME,
    email_sent BOOLEAN DEFAULT FALSE,
    sms_sent BOOLEAN DEFAULT FALSE,
    push_sent BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    FOREIGN KEY (related_request_id) REFERENCES requests_bloodrequest(id) ON DELETE SET NULL,
    INDEX idx_user_read (user_id, is_read),
    INDEX idx_type_priority (notification_type, priority),
    INDEX idx_created_at (created_at)
);
```

## Key Optimizations

### 1. Indexing Strategy
- **Composite Indexes**: For frequent query combinations
- **Spatial Indexes**: For location-based searches
- **Foreign Key Indexes**: For relationship performance
- **Status/Type Indexes**: For filtering operations

### 2. Data Types
- **ENUM**: For fixed option fields (better performance than VARCHAR)
- **DECIMAL**: For precise geographic coordinates
- **DATETIME**: For timezone-aware timestamp storage
- **TEXT**: For variable-length content

### 3. Constraints
- **Foreign Keys**: Maintain referential integrity
- **NOT NULL**: Where data is required
- **DEFAULTS**: Sensible defaults for optional fields
- **UNIQUE**: Prevent duplicate critical data

### 4. Performance Features
- **Partitioning**: Consider for large datasets
- **Caching Keys**: Designed for Redis caching
- **Audit Fields**: Created/updated timestamps
- **Soft Deletes**: Archive flag instead of hard delete

## Relationship Diagram

```
accounts_user (1) ←→ (N) donors_donorhistory
accounts_user (1) ←→ (N) requests_bloodrequest
accounts_user (1) ←→ (N) notifications_notification
requests_bloodrequest (1) ←→ (N) notifications_notification
```

## GDPR Compliance Features

- **Data Minimization**: Only essential fields stored
- **Consent Tracking**: Explicit consent fields
- **Data Retention**: Configurable expiration dates
- **Right to Erasure**: Soft delete capability
- **Audit Trail**: Comprehensive logging

## Scalability Considerations

- **Read Replicas**: Schema supports read scaling
- **Sharding**: User ID based sharding possible
- **Caching**: Redis-optimized field structures
- **Archiving**: Old data archiving strategy
- **Monitoring**: Performance metric fields included

This schema provides a solid foundation for a production-ready blood donation platform with emphasis on performance, data integrity, and regulatory compliance.