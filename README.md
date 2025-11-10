# 🎓 Student Information System (SIS)

A comprehensive web-based Student Information System built with Django and modern frontend technologies. Manage students, track attendance, record grades, and generate reports with an intuitive interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.6-green.svg)

## ✨ Features

### 🎯 Core Functionality
- **Student Management** - Add, edit, view, and delete student records
- **Attendance Tracking** - Mark and monitor student attendance
- **Grade Management** - Record and track student marks/grades
- **Multi-Role Authentication** - Separate portals for Students, Faculty, and Admins
- **Real-time Analytics** - Interactive charts and performance dashboards

### 🎨 UI/UX Features
- **Modern Design** - Purple gradient theme with smooth animations
- **Dark Mode** - Toggle between light and dark themes
- **Responsive Layout** - Mobile-friendly design
- **Advanced Search** - Filter students by class, department, gender
- **Export/Print** - Export to CSV and print-optimized layouts
- **Interactive Charts** - Chart.js integration for data visualization

### 👥 User Roles
1. **Students** - View personal records, attendance, and grades
2. **Faculty** - Manage assigned classes and students
3. **Admins** - Full system access and control

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/student-information-system.git
cd student-information-system
```

2. **Set up virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r sis_backend/requirements.txt
```

4. **Configure MySQL Database**
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE sis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'sis_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON sis_db.* TO 'sis_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

5. **Update database settings**
Edit `sis_backend/sis_backend/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sis_db',
        'USER': 'sis_user',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

6. **Run migrations**
```bash
cd sis_backend
python manage.py migrate
```

7. **Create superuser**
```bash
python manage.py createsuperuser
# Username: devadmin
# Password: Admin123!
```

8. **Load sample data (optional)**
```bash
python manage.py populate_data
python manage.py create_student_users
```

9. **Run development server**
```bash
python manage.py runserver
```

10. **Access the application**
- Frontend: http://127.0.0.1:8000/login.html
- Admin Panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
SIS - Copy/
├── sis_backend/                 # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── sis_backend/            # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── students/               # Main app
│       ├── models.py           # Student, Attendance, Marks models
│       ├── views.py            # View logic
│       ├── api_views.py        # REST API endpoints
│       ├── serializers.py      # DRF serializers
│       └── management/
│           └── commands/
│               └── populate_data.py
├── sis_frontend_detailed - Copy/  # Frontend files
│   ├── index.html              # Dashboard
│   ├── login.html              # Login portal
│   ├── students.html           # Student list
│   ├── add_student.html        # Add student form
│   ├── student_profile.html    # Student details
│   ├── attendance.html         # Attendance page
│   ├── marks.html              # Marks entry
│   └── assets/
│       ├── css/
│       │   └── style.css       # Main stylesheet
│       └── js/
│           └── script.js       # Frontend logic
├── .gitignore
├── README.md
└── IMPROVEMENTS.md
```

## 🔐 Default Credentials

### Admin
- **URL**: `/admin/`
- **Username**: `devadmin`
- **Password**: `Admin123!`

### Faculty
- **URL**: `/login.html`
- **Email**: Check admin panel for faculty accounts
- **Password**: Set by admin

### Student
- **URL**: `/login.html`
- **PRN**: Student enrollment number
- **Password**: `student123` (default)

## 📊 API Endpoints

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

### Attendance
- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Mark attendance

### Marks
- `GET /api/marks/` - List marks
- `POST /api/marks/` - Add marks

## 🎨 Technologies Used

### Backend
- **Django 5.2.6** - Web framework
- **Django REST Framework** - API development
- **MySQL** - Database
- **Python 3.x** - Programming language

### Frontend
- **Bootstrap 5.3.2** - UI framework
- **Chart.js 4.4.0** - Data visualization
- **Bootstrap Icons** - Icon library
- **Vanilla JavaScript** - Client-side logic
- **Google Fonts (Inter)** - Typography

## 🌟 Features Highlights

### Dashboard
- Real-time performance charts (attendance & marks)
- Top performers leaderboard
- Quick stats cards
- Recent activity feed
- Quick action buttons

### Student Management
- Advanced search and filtering
- Multi-criteria filters (class, department, gender)
- Export to CSV
- Print-friendly layout
- Loading states and animations

### Design System
- Purple gradient theme (#667eea, #f093fb)
- Dark mode support
- Smooth transitions and animations
- Responsive grid layout
- Professional typography

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## 📝 Recent Improvements

See [IMPROVEMENTS.md](IMPROVEMENTS.md) for detailed changelog of recent features:
- ✅ Chart.js integration
- ✅ Dark mode implementation
- ✅ Advanced search & filtering
- ✅ CSV export functionality
- ✅ Print optimization
- ✅ Loading states
- ✅ 3-portal login system

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Bootstrap team for the amazing UI framework
- Django community for excellent documentation
- Chart.js for beautiful charts
- All contributors who helped improve this project

## 📞 Support

For support, email your-email@example.com or open an issue in the repository.

---

**Made with ❤️ using Django and modern web technologies**
