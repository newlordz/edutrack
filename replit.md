# EduLearn - Learning Management System

## Overview

EduLearn is a comprehensive Learning Management System (LMS) built with Flask that enables students to browse, enroll in, and track their progress through online courses. The application provides user authentication, course management, enrollment tracking, and grade management functionality with a modern, responsive web interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional Flask web application architecture with the following key components:

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: SQLite (default) with support for PostgreSQL via environment configuration
- **Authentication**: Session-based authentication with password hashing using Werkzeug
- **Application Structure**: Modular design with separate files for models, routes, and application configuration

### Frontend Architecture
- **Template Engine**: Jinja2 templates with inheritance-based layout system
- **CSS Framework**: Bootstrap 5 with dark theme support
- **Icons**: Font Awesome for consistent iconography
- **JavaScript**: Vanilla JavaScript with Bootstrap components for interactive elements

## Key Components

### Database Models
- **User**: Manages student accounts with authentication and profile information
- **Course**: Stores course details including title, description, instructor, and enrollment limits
- **Enrollment**: Tracks student course enrollments with progress tracking
- **Grade**: Manages assignment grades and academic performance

### Core Features
- **User Registration/Login**: Complete authentication system with password security
- **Course Catalog**: Browse and search courses with filtering by difficulty level
- **Enrollment Management**: Students can enroll in courses and track progress
- **Grade Tracking**: View grades and academic performance across enrolled courses
- **Dashboard**: Personalized student dashboard with learning statistics

### UI Components
- **Responsive Design**: Bootstrap-based responsive layout that works on all devices
- **Dark Theme**: Consistent dark theme throughout the application
- **Progressive Enhancement**: JavaScript enhancements for better user experience
- **Accessibility**: Proper ARIA labels and semantic HTML structure

## Data Flow

1. **User Registration**: New users create accounts with validation and password hashing
2. **Authentication**: Session-based login system stores user state
3. **Course Discovery**: Users browse courses with search and filtering capabilities
4. **Enrollment Process**: Students enroll in courses with capacity management
5. **Progress Tracking**: System tracks student progress through enrolled courses
6. **Grade Management**: Instructors can assign grades that students can view

## External Dependencies

### Python Packages
- **Flask**: Web framework for the application
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: Security utilities for password hashing and proxy handling

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for consistent UI elements
- **Custom CSS**: Application-specific styling and animations

### Database
- **PostgreSQL**: Production database connected and configured via DATABASE_URL environment variable
- **Database Tables**: Users, Courses, Enrollments, Grades with proper relationships and constraints

## Deployment Strategy

### Configuration Management
- Environment-based configuration using os.environ
- Separate settings for development (SQLite) and production (PostgreSQL)
- Configurable session secrets and database connection parameters

### Application Structure
- **Entry Point**: main.py imports and runs the Flask application
- **Application Factory**: app.py creates and configures the Flask app
- **Database Initialization**: Automatic table creation and sample data population
- **Static Assets**: CSS and JavaScript files served through Flask's static file handling

### Production Considerations
- ProxyFix middleware for deployment behind reverse proxies
- Database connection pooling and health checks
- Session security with configurable secret keys
- Logging configuration for debugging and monitoring

The application is designed to be easily deployable on platforms like Replit, Heroku, or similar cloud platforms with minimal configuration changes.