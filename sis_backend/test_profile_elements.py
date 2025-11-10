#!/usr/bin/env python
"""Test profile page elements"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis_backend.settings')
django.setup()

from django.test import Client

c = Client()
c.post('/students/login/', {'prn': '14002230001', 'password': 'student123'})
resp = c.get('/students/profile/')
content = resp.content.decode('utf-8')

print('Status Code:', resp.status_code)
print('Has heroName:', 'id="heroName"' in content)
print('Has heroEnrollment:', 'id="heroEnrollment"' in content)
print('Has statAttendance:', 'id="statAttendance"' in content)
print('Has statCGPA:', 'id="statCGPA"' in content)
print('Has subjectsContainer:', 'id="subjectsContainer"' in content)
print('Has attendanceChart:', 'id="attendanceChart"' in content)
print('Has Chart.js:', 'chart.js' in content.lower())
print('Has Bootstrap:', 'bootstrap' in content.lower())
print('Profile API fetch:', '/api/student-profile/' in content)
