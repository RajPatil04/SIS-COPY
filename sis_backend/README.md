Django backend for SIS integrated with MySQL

Overview
- Project: `sis_backend`
- App: `students` (models for Student, Attendance, Mark)
- The frontend files live in `../sis_frontend_detailed - Copy` and are used as templates/static assets.

Assumptions
- You're on Windows (cmd.exe)
- MySQL server is installed and accessible
- We'll use `PyMySQL` as the DB adapter (no C build tools required)

Quick setup (cmd.exe)
1) Create & activate a virtualenv (recommended):
   python -m venv venv
   venv\Scripts\activate

2) Install dependencies:
   pip install -r requirements.txt

3) Create a MySQL database and user (replace values as needed):
   -- run these in your MySQL client:
   CREATE DATABASE sis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'sis_user'@'localhost' IDENTIFIED BY 'changeme';
   GRANT ALL PRIVILEGES ON sis_db.* TO 'sis_user'@'localhost';
   FLUSH PRIVILEGES;

4) Update `DATABASES` in `sis_backend/sis_backend/settings.py` if you changed credentials.

5) Run migrations:
   python manage.py migrate

6) Create a superuser:
   python manage.py createsuperuser

7) Run the dev server:
   python manage.py runserver

Notes
- If PyMySQL gives trouble, you can install `mysqlclient` instead but you will need Visual C++ build tools on Windows.
- Next steps: implement REST APIs for the frontend forms, add authentication, and small tests.

API endpoints
- After installing `djangorestframework` (already included in `requirements.txt`), the backend exposes REST endpoints under the `/api/` prefix. Example routes:
   - GET /api/students/ — list students
   - POST /api/students/ — create student
   - GET /api/students/{id}/ — retrieve student
   - PUT /api/students/{id}/ — update student
   - DELETE /api/students/{id}/ — delete student

The frontend is modified to attempt calling `/api/students/` and will fall back to the localStorage demo data if the API is not available.

SQLite fallback (quick local run)
- If you don't want to configure MySQL yet, you can use the built-in SQLite DB for quick testing.
- Enable it by setting the environment variable `USE_SQLITE=1` before running migrations.

On Windows cmd.exe:
```
set USE_SQLITE=1
venv\Scripts\activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

When using SQLite the app will create `db.sqlite3` in the `sis_backend` folder.
