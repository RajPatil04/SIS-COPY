#!/usr/bin/env python
"""Display complete database contents"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sis_backend.settings')
django.setup()

from students.models import Student, Attendance, Mark
from django.contrib.auth.models import User

print("=" * 80)
print("DATABASE CONTENTS")
print("=" * 80)

# Summary
print("\n📊 SUMMARY:")
print(f"   Students: {Student.objects.count()}")
print(f"   Users: {User.objects.count()}")
print(f"   Attendance Records: {Attendance.objects.count()}")
print(f"   Marks Records: {Mark.objects.count()}")

# Students by section
print("\n👥 STUDENTS BY SECTION:")
sections = Student.objects.values_list('section', flat=True).distinct().order_by('section')
for section in sections:
    count = Student.objects.filter(section=section).count()
    print(f"   {section}: {count} students")

# Sample Students
print("\n📝 FIRST 10 STUDENTS:")
print(f"{'SAP ID':<15} {'Name':<30} {'Section':<15} {'Email':<30}")
print("-" * 90)
for s in Student.objects.all().order_by('enrollment_number')[:10]:
    name = f"{s.first_name} {s.last_name}"
    email = s.email or "N/A"
    print(f"{s.enrollment_number:<15} {name:<30} {s.section:<15} {email:<30}")

# Sample Attendance
print("\n📅 SAMPLE ATTENDANCE (First student, recent 5 days):")
first_student = Student.objects.first()
if first_student:
    print(f"   Student: {first_student.first_name} {first_student.last_name} ({first_student.enrollment_number})")
    attendance = Attendance.objects.filter(student=first_student).order_by('-date')[:5]
    for att in attendance:
        status = "✓ Present" if att.present else "✗ Absent"
        print(f"   {att.date} ({att.date.strftime('%A')}): {status}")

# Sample Marks
print("\n📊 SAMPLE MARKS (First student):")
if first_student:
    marks = Mark.objects.filter(student=first_student)
    if marks.exists():
        total_percentage = 0
        for mark in marks:
            percentage = (mark.marks_obtained / mark.max_marks * 100)
            total_percentage += percentage
            print(f"   {mark.subject}: {mark.marks_obtained}/{mark.max_marks} ({percentage:.1f}%)")
        
        avg_percentage = total_percentage / marks.count()
        cgpa = avg_percentage / 10
        print(f"\n   Average: {avg_percentage:.2f}%")
        print(f"   CGPA: {cgpa:.2f}/10")
    else:
        print("   No marks data")

# User Accounts
print("\n🔐 SAMPLE USER ACCOUNTS (Student logins):")
print(f"{'Username':<15} {'Is Active':<10} {'Is Staff':<10} {'Last Login':<25}")
print("-" * 70)
for u in User.objects.filter(username__startswith="14002230").order_by('username')[:5]:
    last_login = u.last_login.strftime('%Y-%m-%d %H:%M') if u.last_login else 'Never'
    print(f"{u.username:<15} {str(u.is_active):<10} {str(u.is_staff):<10} {last_login:<25}")

# Faculty/Admin Users
print("\n👨‍🏫 FACULTY/ADMIN USERS:")
faculty_users = User.objects.filter(is_staff=True) | User.objects.filter(is_superuser=True)
if faculty_users.exists():
    for u in faculty_users:
        role = "Superuser" if u.is_superuser else "Staff"
        print(f"   {u.username} ({u.email}) - {role}")
else:
    print("   No faculty/admin users")

# Statistics
print("\n📈 ATTENDANCE STATISTICS:")
total_att = Attendance.objects.count()
present_att = Attendance.objects.filter(present=True).count()
if total_att > 0:
    overall_percentage = (present_att / total_att * 100)
    print(f"   Overall Attendance: {overall_percentage:.1f}%")
    print(f"   Present: {present_att} / {total_att}")

print("\n📊 MARKS STATISTICS:")
if Mark.objects.exists():
    from django.db.models import Avg
    avg_marks = Mark.objects.aggregate(
        avg_obtained=Avg('marks_obtained'),
        avg_max=Avg('max_marks')
    )
    if avg_marks['avg_obtained'] and avg_marks['avg_max']:
        avg_percentage = (avg_marks['avg_obtained'] / avg_marks['avg_max']) * 100
        print(f"   Average Marks: {avg_percentage:.2f}%")
        print(f"   Average CGPA: {avg_percentage/10:.2f}/10")

print("\n" + "=" * 80)
print("END OF DATABASE REPORT")
print("=" * 80)
