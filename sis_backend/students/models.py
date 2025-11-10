from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # Extended fields to match frontend
    class_year = models.CharField(max_length=120, blank=True, null=True)
    department = models.CharField(max_length=120, blank=True, null=True)
    semester = models.PositiveSmallIntegerField(blank=True, null=True)
    # Section/class code, e.g. "SY-COMP-A" or "TY-COMP-B"
    section = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    def calculate_cgpa(self):
        """Calculate CGPA based on all marks (10-point scale)"""
        marks = self.marks.all()
        if not marks:
            return 0.0
        
        total_percentage = sum((m.marks_obtained / m.max_marks * 100) for m in marks)
        avg_percentage = total_percentage / marks.count()
        
        # Convert percentage to CGPA (10-point scale)
        # 90-100% = 10, 80-89% = 9, 70-79% = 8, etc.
        cgpa = avg_percentage / 10
        return round(cgpa, 2)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.enrollment_number})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {'Present' if self.present else 'Absent'}"


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=200)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.DecimalField(max_digits=6, decimal_places=2, default=100)

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.marks_obtained}/{self.max_marks}"


class FacultyProfile(models.Model):
    """
    Lightweight profile for faculty/staff users that records which subjects and
    classes/sections they are responsible for.

    - user: linked Django User (faculty account)
    - subjects: comma-separated subject names (e.g. "Data Structures,DAA")
    - classes: comma-separated class/section identifiers (e.g. "SY-COMP-A,SY-COMP-B,TY-COMP-A")
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    subjects = models.TextField(blank=True, help_text='Comma-separated list of subjects')
    classes = models.TextField(blank=True, help_text='Comma-separated list of classes/sections')

    def get_subject_list(self):
        return [s.strip() for s in (self.subjects or '').split(',') if s.strip()]

    def get_class_list(self):
        return [c.strip() for c in (self.classes or '').split(',') if c.strip()]

    def __str__(self):
        return f"FacultyProfile({self.user.username})"
