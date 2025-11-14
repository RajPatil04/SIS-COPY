from rest_framework import viewsets, permissions
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.db.models import Avg, Count, Q
from datetime import datetime, timedelta
from .models import Student, Attendance, Mark
from .serializers import StudentSerializer, AttendanceSerializer, MarkSerializer


@method_decorator(csrf_exempt, name='dispatch')
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    # Use DjangoModelPermissionsOrAnonReadOnly: anonymous users can read; authenticated users require model perms to write
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        """Scope queryset based on current user:
        - If faculty (has faculty_profile): return students whose `section` is in their allowed classes
        - If student user (username == enrollment_number): return only that student's record
        - Else (admin or anonymous): return all students
        """
        user = getattr(self.request, 'user', None)
        qs = Student.objects.all().order_by('id')
        # Always return full list for list action so frontend can display all students.
        # Object-level scoping is still enforced for create/update/delete via perform_* methods.
        if getattr(self, 'action', None) == 'list':
            return qs
        if not user or not user.is_authenticated:
            return qs

        # Student user
        try:
            student = Student.objects.get(enrollment_number=user.username)
            return qs.filter(pk=student.pk)
        except Student.DoesNotExist:
            pass

        # Faculty user with FacultyProfile
        if hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if allowed:
                return qs.filter(section__in=allowed)

        # Default: return all (admins)
        return qs

    def perform_create(self, serializer):
        # If faculty, ensure target student is in allowed classes
        user = getattr(self.request, 'user', None)
        student = serializer.validated_data.get('student')
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot modify student outside your classes')
        serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        instance = serializer.instance
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot modify student outside your classes')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot delete student outside your classes')
        instance.delete()


@method_decorator(csrf_exempt, name='dispatch')
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        qs = Attendance.objects.all().order_by('-date')
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return qs

        # Student: only their attendance
        try:
            student = Student.objects.get(enrollment_number=user.username)
            return qs.filter(student=student)
        except Student.DoesNotExist:
            pass

        # Faculty: only attendance for students in their classes
        if hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if allowed:
                return qs.filter(student__section__in=allowed)

        return qs

    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        student = serializer.validated_data.get('student')
        # If faculty, ensure student is in allowed classes
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot add attendance for students outside your classes')
        serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        instance = serializer.instance
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot edit attendance for students outside your classes')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot delete attendance for students outside your classes')
        instance.delete()


@method_decorator(csrf_exempt, name='dispatch')
class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        qs = Mark.objects.all().order_by('id')
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return qs

        # Student: only their marks
        try:
            student = Student.objects.get(enrollment_number=user.username)
            return qs.filter(student=student)
        except Student.DoesNotExist:
            pass

        # Faculty: only marks for students in their allowed classes
        if hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if allowed:
                return qs.filter(student__section__in=allowed)

        return qs

    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        student = serializer.validated_data.get('student')
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot add marks for students outside your classes')
        serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        instance = serializer.instance
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot edit marks for students outside your classes')
        serializer.save()

    def perform_destroy(self, instance):
        user = getattr(self.request, 'user', None)
        if user and hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if instance.student.section not in allowed:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('Cannot delete marks for students outside your classes')
        instance.delete()


def whoami(request):
    """Simple endpoint returning current user and groups for frontend role checks."""
    if not request.user or not request.user.is_authenticated:
        return JsonResponse({'is_authenticated': False})

    groups = list(request.user.groups.values_list('name', flat=True))
    return JsonResponse({'is_authenticated': True, 'username': request.user.username, 'groups': groups})


def performance_analytics(request):
    """
    API endpoint for dashboard performance analytics.
    Returns attendance and marks data for the last 6 days.
    Filters by year and division if provided.
    """
    year_filter = request.GET.get('year', '')  # FY, SY, TY
    division_filter = request.GET.get('division', '')  # A, B, C
    
    # Build filter based on class_year and section fields
    students = Student.objects.all()
    
    if year_filter:
        students = students.filter(class_year__startswith=year_filter)
    
    if division_filter:
        # Section format is like "TY-COMP-A", "SY-COMP-B", etc.
        students = students.filter(section__endswith=f"-{division_filter}")
    
    student_ids = list(students.values_list('id', flat=True))
    
    # Get last 6 days of data
    today = datetime.now().date()
    days_data = []
    labels = []
    
    for i in range(6):
        date = today - timedelta(days=5-i)
        labels.append(date.strftime('%a'))  # Mon, Tue, Wed, etc.
        
        # Calculate attendance percentage for this day
        total_attendance = Attendance.objects.filter(
            student_id__in=student_ids,
            date=date
        )
        total_count = total_attendance.count()
        present_count = total_attendance.filter(present=True).count()
        
        attendance_pct = round((present_count / total_count * 100), 1) if total_count > 0 else 0
        days_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'attendance': attendance_pct
        })
    
    # Calculate CGPA for each day (using all marks data, not day-specific)
    cgpa_data = []
    for day_info in days_data:
        # Get marks for these students and calculate average CGPA
        total_cgpa = 0
        cgpa_count = 0
        
        for student_id in student_ids:
            marks = Mark.objects.filter(student_id=student_id)
            if marks.exists():
                # Calculate percentage and convert to CGPA (10-point scale)
                total_percentage = sum((m.marks_obtained / m.max_marks * 100) for m in marks)
                avg_percentage = total_percentage / marks.count()
                cgpa = avg_percentage / 10
                total_cgpa += cgpa
                cgpa_count += 1
        
        avg_cgpa = round((total_cgpa / cgpa_count), 2) if cgpa_count > 0 else 0.0
        cgpa_data.append(float(avg_cgpa))  # Ensure it's a float, not Decimal
    
    # Extract attendance percentages
    attendance_data = [day['attendance'] for day in days_data]
    
    return JsonResponse({
        'labels': labels,
        'attendance': attendance_data,
        'cgpa': cgpa_data,
        'filter': {
            'year': year_filter,
            'division': division_filter,
            'student_count': len(student_ids)
        }
    })


@csrf_exempt
@require_http_methods(["GET"])
def student_profile_data(request):
    """
    API endpoint to get the logged-in student's profile data.
    Returns student info, attendance, marks, and calculated metrics.
    """
    # If the request is not authenticated, return JSON 401 instead of redirecting to login HTML
    # Debug: log incoming cookies and session to help client-side debugging
    try:
        print('DEBUG: Request.COOKIES:', request.COOKIES)
        print('DEBUG: HTTP_COOKIE header:', request.META.get('HTTP_COOKIE'))
        print('DEBUG: session_key:', getattr(request.session, 'session_key', None))
    except Exception as e:
        print('DEBUG: Could not print cookies/session:', e)

    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    # Debug logging
    print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
    print(f"DEBUG: Username: {request.user.username}")

    # Get the student record for the logged-in user
    try:
        student = Student.objects.get(enrollment_number=request.user.username)
        print(f"DEBUG: Found student: {student.first_name} {student.last_name}")
    except Student.DoesNotExist:
        print(f"DEBUG: Student not found for username: {request.user.username}")
        return JsonResponse({'error': 'Student record not found'}, status=404)
    
    # Calculate attendance percentage
    total_attendance = Attendance.objects.filter(student=student)
    attendance_count = total_attendance.count()
    present_count = total_attendance.filter(present=True).count()
    attendance_percentage = round((present_count / attendance_count * 100), 1) if attendance_count > 0 else 0.0
    
    # Get marks and calculate CGPA
    marks = Mark.objects.filter(student=student)
    if marks.exists():
        total_percentage = sum((m.marks_obtained / m.max_marks * 100) for m in marks)
        avg_percentage = total_percentage / marks.count()
        cgpa = round(avg_percentage / 10, 2)
    else:
        cgpa = 0.0
    
    # Get subject-wise marks
    subjects_data = []
    for mark in marks:
        subjects_data.append({
            'name': mark.subject,
            'marks': int(mark.marks_obtained),
            'total': int(mark.max_marks)
        })
    
    # Get recent attendance records (last 10 days)
    recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:10]
    attendance_records = []
    for record in recent_attendance:
        attendance_records.append({
            'date': record.date.strftime('%Y-%m-%d'),
            'present': record.present,
            'day': record.date.strftime('%A')
        })
    
    # Prepare response data
    data = {
        'name': f"{student.first_name} {student.last_name}",
        'enrollment': student.enrollment_number,
        'class': student.class_year or 'TY Computer',
        'department': student.department or 'Computer Engineering',
        'section': student.section or 'N/A',
        'email': student.email or f"{student.enrollment_number.lower()}@college.edu",
        'contact': student.contact or 'Not provided',
        'dob': student.date_of_birth.strftime('%Y-%m-%d') if student.date_of_birth else 'Not provided',
        'gender': student.gender or 'Not specified',
        'address': student.address or 'Not provided',
        'semester': student.semester if student.semester else 5,
        'cgpa': cgpa,
        'attendance': attendance_percentage,
        'rank': 'N/A',  # Can be calculated later based on class ranking
        'subjects': subjects_data,
        'recentAttendance': attendance_records
    }
    
    return JsonResponse(data)

