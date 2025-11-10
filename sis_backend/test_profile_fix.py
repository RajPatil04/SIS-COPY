#!/usr/bin/env python
"""Test script to verify student profile page fix"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis_backend.settings')
django.setup()

from django.test import Client

def test_profile_flow():
    client = Client()
    
    print("=" * 60)
    print("TESTING STUDENT PROFILE FIX")
    print("=" * 60)
    
    # Test 1: Student Login
    print("\n1. Testing Student Login (SAP ID: 14002230001)")
    resp = client.post('/students/login/', {
        'prn': '14002230001',
        'password': 'student123'
    })
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 302:
        print(f"   Redirect: {resp.url}")
        print(f"   ✅ Login successful" if '/students/profile/' in resp.url else "   ❌ Wrong redirect")
    
    # Test 2: Profile Page Access
    print("\n2. Testing Profile Page Access")
    profile_resp = client.get('/students/profile/')
    print(f"   Status: {profile_resp.status_code}")
    print(f"   ✅ Profile accessible" if profile_resp.status_code == 200 else f"   ❌ Profile not accessible")
    
    # Test 3: Profile API Data
    print("\n3. Testing Profile API")
    api_resp = client.get('/api/student-profile/')
    print(f"   Status: {api_resp.status_code}")
    
    if api_resp.status_code == 200:
        data = api_resp.json()
        print(f"   ✅ API working")
        print(f"\n   Student Details:")
        print(f"   - Name: {data['name']}")
        print(f"   - Enrollment: {data['enrollment']}")
        print(f"   - Class: {data['class']} {data['section']}")
        print(f"   - CGPA: {data['cgpa']}")
        print(f"   - Attendance: {data['attendance']}%")
        print(f"   - Subjects: {len(data['subjects'])}")
        print(f"   - Attendance Records: {len(data['recentAttendance'])}")
    else:
        print(f"   ❌ API failed")
    
    # Test 4: Different Student
    print("\n4. Testing Different Student (SAP ID: 14002230039)")
    client2 = Client()
    resp2 = client2.post('/students/login/', {
        'prn': '14002230039',
        'password': 'student123'
    })
    
    if resp2.status_code == 302:
        api_resp2 = client2.get('/api/student-profile/')
        if api_resp2.status_code == 200:
            data2 = api_resp2.json()
            print(f"   Name: {data2['name']}")
            print(f"   Enrollment: {data2['enrollment']}")
            print(f"   CGPA: {data2['cgpa']}")
            
            if data['name'] != data2['name']:
                print(f"   ✅ Different students get different data")
            else:
                print(f"   ❌ Same data for different students")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    test_profile_flow()
