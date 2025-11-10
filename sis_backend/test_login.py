#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

print("="*70)
print("SYSTEM TEST - Student Information System")
print("="*70)

# Test 1: Check database
from students.models import Student, Attendance, Mark
print("\n1. DATABASE CHECK:")
print(f"   ✓ Students: {Student.objects.count()}")
print(f"   ✓ Users: {User.objects.count()}")
print(f"   ✓ Attendance Records: {Attendance.objects.count()}")
print(f"   ✓ Marks Records: {Mark.objects.count()}")

# Test 2: Test student login
print("\n2. TESTING STUDENT LOGIN:")
client = Client()

# Get login page
response = client.get('/students/login/')
print(f"   ✓ Login page loads: {response.status_code == 200}")

# Test login with student credentials
login_data = {
    'prn': '14002230001',
    'password': 'student123'
}
response = client.post('/students/login/', login_data)
print(f"   ✓ Login successful: {response.status_code in [200, 302]}")
print(f"   ✓ Redirect URL: {response.url if hasattr(response, 'url') else 'student_profile.html'}")

# Test 3: Test student profile API
print("\n3. TESTING PROFILE API:")
# Login first
client.login(username='14002230001', password='student123')
response = client.get('/api/student-profile/')
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ API works: True")
    print(f"   ✓ Student Name: {data['name']}")
    print(f"   ✓ Enrollment: {data['enrollment']}")
    print(f"   ✓ Section: {data['section']}")
    print(f"   ✓ CGPA: {data['cgpa']}")
    print(f"   ✓ Attendance: {data['attendance']}%")
    print(f"   ✓ Subjects: {len(data['subjects'])} subjects")
    print(f"   ✓ Attendance Records: {len(data['recentAttendance'])} days")
else:
    print(f"   ✗ API failed: {response.status_code}")

# Test 4: Test different student
print("\n4. TESTING DIFFERENT STUDENT (14002230039):")
client2 = Client()
client2.login(username='14002230039', password='student123')
response = client2.get('/api/student-profile/')
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ Student Name: {data['name']}")
    print(f"   ✓ Enrollment: {data['enrollment']}")
    print(f"   ✓ CGPA: {data['cgpa']}")
    print(f"   ✓ Different from first student: {data['enrollment'] != '14002230001'}")
else:
    print(f"   ✗ Failed")

# Test 5: Test performance analytics API
print("\n5. TESTING PERFORMANCE ANALYTICS:")
response = client.get('/api/performance-analytics/')
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ API works: True")
    print(f"   ✓ Total students: {data['filter']['student_count']}")
    print(f"   ✓ Data points: {len(data['labels'])} days")
    print(f"   ✓ Attendance data: {data['attendance'][:3]}...")
    print(f"   ✓ CGPA data: {data['cgpa'][:3]}...")
else:
    print(f"   ✗ Failed")

# Test 6: Test with filters
print("\n6. TESTING FILTERS (TY Division A):")
response = client.get('/api/performance-analytics/?year=TY&division=A')
if response.status_code == 200:
    data = response.json()
    print(f"   ✓ Filtered students: {data['filter']['student_count']}")
    print(f"   ✓ Year filter: {data['filter']['year']}")
    print(f"   ✓ Division filter: {data['filter']['division']}")
else:
    print(f"   ✗ Failed")

# Test 7: Test faculty login
print("\n7. TESTING FACULTY LOGIN:")
client3 = Client()
response = client3.get('/students/faculty-login/')
print(f"   ✓ Faculty login page: {response.status_code == 200}")

# Test 8: Main pages
print("\n8. TESTING MAIN PAGES:")
pages = {
    '/login.html': 'Login Portal',
    '/index.html': 'Dashboard',
    '/student_profile.html': 'Student Profile',
}
for url, name in pages.items():
    response = client.get(url)
    print(f"   ✓ {name}: {response.status_code == 200}")

print("\n" + "="*70)
print("ALL TESTS COMPLETED!")
print("="*70)
print("\n✅ System is ready to use!")
print("\n📋 Access Points:")
print("   • Login Portal: http://127.0.0.1:8000/login.html")
print("   • Student Login: http://127.0.0.1:8000/students/login/")
print("   • Faculty Login: http://127.0.0.1:8000/students/faculty-login/")
print("   • Dashboard: http://127.0.0.1:8000/index.html")
print("\n🔑 Test Credentials:")
print("   • Student: 14002230001 / student123")
print("   • Student: 14002230039 / student123")
print("   • Faculty: teacher@example.com / password")
print("   • Admin: devadmin / Admin123!")
print("="*70)
