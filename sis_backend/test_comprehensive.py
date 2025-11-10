#!/usr/bin/env python
"""Comprehensive test to find and report all errors in the system"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from students.models import Student, Attendance, Mark
import json

def test_all():
    print("=" * 70)
    print("COMPREHENSIVE SYSTEM ERROR CHECK")
    print("=" * 70)
    
    errors = []
    warnings = []
    
    # Test 1: Database Models
    print("\n1. Testing Database Models...")
    try:
        student_count = Student.objects.count()
        user_count = User.objects.count()
        attendance_count = Attendance.objects.count()
        mark_count = Mark.objects.count()
        
        print(f"   ✅ Students: {student_count}")
        print(f"   ✅ Users: {user_count}")
        print(f"   ✅ Attendance: {attendance_count}")
        print(f"   ✅ Marks: {mark_count}")
        
        if student_count == 0:
            errors.append("No students in database")
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
        print(f"   ❌ Database error: {str(e)}")
    
    # Test 2: Student Login
    print("\n2. Testing Student Login...")
    client = Client()
    try:
        # Test login page loads
        resp = client.get('/students/login/')
        if resp.status_code != 200:
            errors.append(f"Login page returns {resp.status_code}")
            print(f"   ❌ Login page: {resp.status_code}")
        else:
            print(f"   ✅ Login page accessible")
        
        # Test login functionality
        resp = client.post('/students/login/', {
            'prn': '14002230001',
            'password': 'student123'
        })
        if resp.status_code == 302:
            print(f"   ✅ Login redirect: {resp.url}")
            if '/students/profile/' not in resp.url:
                warnings.append(f"Login redirects to {resp.url} instead of /students/profile/")
        else:
            errors.append(f"Login failed with status {resp.status_code}")
            print(f"   ❌ Login failed: {resp.status_code}")
    except Exception as e:
        errors.append(f"Login test error: {str(e)}")
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Profile Page
    print("\n3. Testing Profile Page...")
    try:
        resp = client.get('/students/profile/')
        if resp.status_code == 200:
            print(f"   ✅ Profile page loads")
            # Check if essential elements exist
            content = resp.content.decode('utf-8')
            if 'heroName' not in content:
                warnings.append("Profile page missing 'heroName' element")
            if 'statAttendance' not in content:
                warnings.append("Profile page missing 'statAttendance' element")
            if 'subjectsContainer' not in content:
                warnings.append("Profile page missing 'subjectsContainer' element")
        else:
            errors.append(f"Profile page returns {resp.status_code}")
            print(f"   ❌ Profile page: {resp.status_code}")
    except Exception as e:
        errors.append(f"Profile page error: {str(e)}")
        print(f"   ❌ Error: {str(e)}")
    
    # Test 4: Profile API
    print("\n4. Testing Profile API...")
    try:
        resp = client.get('/api/student-profile/')
        if resp.status_code == 200:
            data = resp.json()
            required_fields = ['name', 'enrollment', 'class', 'section', 'cgpa', 'attendance', 'subjects', 'recentAttendance']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                errors.append(f"API missing fields: {missing_fields}")
                print(f"   ❌ Missing fields: {missing_fields}")
            else:
                print(f"   ✅ API returns all fields")
                print(f"   ✅ Student: {data['name']}")
                print(f"   ✅ CGPA: {data['cgpa']}, Attendance: {data['attendance']}%")
        else:
            errors.append(f"Profile API returns {resp.status_code}")
            print(f"   ❌ API error: {resp.status_code}")
    except Exception as e:
        errors.append(f"API test error: {str(e)}")
        print(f"   ❌ Error: {str(e)}")
    
    # Test 5: Faculty Login
    print("\n5. Testing Faculty Login...")
    client2 = Client()
    try:
        resp = client2.get('/students/faculty-login/')
        if resp.status_code == 200:
            print(f"   ✅ Faculty login page accessible")
        else:
            warnings.append(f"Faculty login page returns {resp.status_code}")
            print(f"   ⚠️  Faculty login page: {resp.status_code}")
    except Exception as e:
        warnings.append(f"Faculty login error: {str(e)}")
        print(f"   ⚠️  Error: {str(e)}")
    
    # Test 6: Performance Analytics API
    print("\n6. Testing Performance Analytics...")
    try:
        resp = client.get('/api/performance-analytics/')
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict) and 'labels' in data and 'attendance' in data:
                print(f"   ✅ Analytics API returns data")
                print(f"   ✅ Days: {len(data['labels'])}, Students: {data.get('filter', {}).get('student_count', 0)}")
            else:
                warnings.append("Analytics API returns unexpected format")
                print(f"   ⚠️  Unexpected data format")
        else:
            warnings.append(f"Analytics API returns {resp.status_code}")
            print(f"   ⚠️  Analytics API: {resp.status_code}")
    except Exception as e:
        warnings.append(f"Analytics API error: {str(e)}")
        print(f"   ⚠️  Error: {str(e)}")
    
    # Test 7: Check for students with missing data
    print("\n7. Checking Student Data Quality...")
    try:
        # Use 'marks' instead of 'mark' (correct field name)
        students_no_marks = Student.objects.filter(marks__isnull=True).distinct().count()
        students_no_attendance = Student.objects.filter(attendances__isnull=True).distinct().count()
        
        if students_no_marks > 0:
            warnings.append(f"{students_no_marks} students have no marks")
            print(f"   ⚠️  {students_no_marks} students without marks")
        else:
            print(f"   ✅ All students have marks")
        
        if students_no_attendance > 0:
            warnings.append(f"{students_no_attendance} students have no attendance")
            print(f"   ⚠️  {students_no_attendance} students without attendance")
        else:
            print(f"   ✅ All students have attendance records")
    except Exception as e:
        warnings.append(f"Data quality check error: {str(e)}")
        print(f"   ⚠️  Error: {str(e)}")
    
    # Test 8: URL Routing
    print("\n8. Testing URL Routes...")
    routes_to_test = [
        ('/', 'Homepage'),
        ('/students/login/', 'Student Login'),
        ('/students/faculty-login/', 'Faculty Login'),
        ('/api/students/', 'Students API'),
    ]
    
    test_client = Client()
    for url, name in routes_to_test:
        try:
            resp = test_client.get(url)
            if resp.status_code in [200, 302]:
                print(f"   ✅ {name}: {resp.status_code}")
            else:
                warnings.append(f"{name} returns {resp.status_code}")
                print(f"   ⚠️  {name}: {resp.status_code}")
        except Exception as e:
            errors.append(f"{name} error: {str(e)}")
            print(f"   ❌ {name}: {str(e)}")
    
    # Final Report
    print("\n" + "=" * 70)
    print("FINAL REPORT")
    print("=" * 70)
    
    if not errors and not warnings:
        print("\n✅ ALL TESTS PASSED - NO ERRORS OR WARNINGS!")
    else:
        if errors:
            print(f"\n❌ ERRORS FOUND ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")
    
    print("\n" + "=" * 70)
    
    return len(errors) == 0

if __name__ == '__main__':
    success = test_all()
    exit(0 if success else 1)
