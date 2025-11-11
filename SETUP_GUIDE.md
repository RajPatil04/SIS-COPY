# Student Information System - Setup Guide

This guide will help you clone and run the Student Information System on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **MySQL 8.0 or higher**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Remember your root password during installation

3. **Git**
   - Download from: https://git-scm.com/downloads/

## Installation Steps

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
git clone https://github.com/RajPatil04/SIS-PROJECT.git
cd SIS-PROJECT
```

### Step 2: Set Up MySQL Database

1. Open MySQL Command Line or MySQL Workbench
2. Login with your root password
3. Create the database and user:

```sql
CREATE DATABASE sis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sis_user'@'localhost' IDENTIFIED BY 'sis_password123';
GRANT ALL PRIVILEGES ON sis_db.* TO 'sis_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 3: Install Python Dependencies

Navigate to the backend folder and install requirements:

```bash
cd sis_backend
pip install -r requirements.txt
```

**If you get any errors**, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Database Settings (Optional)

If you used different database credentials, update `sis_backend/sis_backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sis_db',
        'USER': 'sis_user',           # Your MySQL username
        'PASSWORD': 'sis_password123', # Your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### Step 5: Run Database Migrations

Apply the database schema:

```bash
python manage.py migrate
```

### Step 6: Create Student Users and Data

Run these management commands to populate the database:

```bash
# Create 124 student user accounts
python manage.py create_student_users

# Populate attendance and marks data
python manage.py populate_performance_data
```

### Step 7: Create Admin/Faculty User (Optional)

To create a superuser for admin access:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### Step 8: Start the Development Server

```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

## Accessing the System

### Student Login
1. Go to: http://127.0.0.1:8000/students/login/
2. **Username**: Any SAP ID from `14002230001` to `14002230124`
3. **Password**: `student123` (same for all students)

### Faculty Login
1. Go to: http://127.0.0.1:8000/students/faculty-login/
2. Use faculty credentials (if created) or create one using admin panel

### Admin Panel
1. Go to: http://127.0.0.1:8000/admin/
2. Use the superuser credentials you created in Step 7

## Common Issues and Solutions

### Issue 1: MySQL Connection Error
**Error**: `Can't connect to MySQL server`

**Solution**:
- Make sure MySQL service is running
- Check database credentials in `settings.py`
- Verify MySQL is listening on port 3306

### Issue 2: Module Not Found Error
**Error**: `ModuleNotFoundError: No module named 'django'`

**Solution**:
```bash
pip install django
pip install -r requirements.txt
```

### Issue 3: Port Already in Use
**Error**: `Error: That port is already in use`

**Solution**:
```bash
# Run on a different port
python manage.py runserver 8080
```

### Issue 4: No Student Data
**Error**: Empty dashboard or no students

**Solution**:
```bash
# Re-run data population commands
python manage.py create_student_users
python manage.py populate_performance_data
```

## Project Structure

```
SIS-PROJECT/
├── sis_backend/              # Django Backend
│   ├── manage.py            # Django management script
│   ├── requirements.txt     # Python dependencies
│   ├── sis_backend/         # Main project settings
│   │   ├── settings.py      # Database & app config
│   │   └── urls.py          # URL routing
│   ├── students/            # Students app
│   │   ├── models.py        # Database models
│   │   ├── views.py         # Views & logic
│   │   ├── api_views.py     # REST API endpoints
│   │   └── management/      # Custom commands
│   └── templates/           # HTML templates
│       ├── student_login.html
│       ├── faculty_login.html
│       └── student_profile.html
└── sis_frontend_detailed - Copy/  # Frontend assets
    ├── assets/
    │   ├── css/            # Stylesheets
    │   └── js/             # JavaScript files
    └── *.html              # HTML pages
```

## Features

✅ **124 Unique Student Accounts** - Each with unique SAP ID  
✅ **Student Dashboard** - View attendance, CGPA, subjects, profile  
✅ **Performance Analytics** - Charts and graphs for tracking  
✅ **Attendance Management** - Track daily attendance  
✅ **Marks/CGPA System** - Automatic CGPA calculation  
✅ **Faculty Portal** - Separate login for faculty  
✅ **Responsive Design** - Works on mobile, tablet, desktop  
✅ **REST API** - JSON endpoints for data access  

## Quick Reference

### Student Credentials
- **SAP IDs**: 14002230001 to 14002230124
- **Password**: student123 (all students)
- **Example**: Login with `14002230001` / `student123`

### Useful Commands
```bash
# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Check for errors
python manage.py check

# Show student logins
python manage.py show_student_logins

# Run migrations
python manage.py migrate

# Create test data
python manage.py populate_performance_data
```

## Need Help?

- Check `SYSTEM_STATUS.md` for detailed system information
- Check `QUICK_REFERENCE.txt` for credentials
- Review Django documentation: https://docs.djangoproject.com/

## Tech Stack

- **Backend**: Django 5.2.6, Django REST Framework
- **Database**: MySQL 8.0+
- **Frontend**: Bootstrap 5.3.2, Chart.js 4.4.0, Vanilla JavaScript
- **Authentication**: Django session-based authentication

---

**Repository**: https://github.com/RajPatil04/SIS-PROJECT  
**Email**: rajnpatil04@gmail.com
