from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.urls import reverse


def index(request):
    # If logged in as a student (username == enrollment_number) redirect to their profile
    if request.user.is_authenticated:
        try:
            student = Student.objects.get(enrollment_number=request.user.username)
            return redirect('students:student_detail', pk=student.pk)
        except Student.DoesNotExist:
            pass

        # If user has a FacultyProfile, show only students in their allowed classes
        if hasattr(request.user, 'faculty_profile'):
            allowed = request.user.faculty_profile.get_class_list()
            students = Student.objects.filter(section__in=allowed).order_by('id')
            return render(request, 'students/list.html', {'students': students})

    # For staff/admin and anonymous visitors show the full students list (for demo)
    # If you want to restrict visibility in production, change this behavior.
    students = Student.objects.all().order_by('id')
    return render(request, 'students/list.html', {'students': students})


@login_required
def students_all(request):
    """Return a full list of students for staff/admin users only."""
    from django.core.exceptions import PermissionDenied

    user = request.user
    # Only staff users can access the full list (faculty should remain scoped)
    if not user.is_staff:
        raise PermissionDenied('You do not have permission to view all students')

    students = Student.objects.all().order_by('id')
    return render(request, 'students/list.html', {'students': students, 'show_all': True})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # Enforce that regular student users can only view their own profile.
    user = request.user
    from django.core.exceptions import PermissionDenied

    if user.is_authenticated:
        # Staff/admin can view any student
        if user.is_staff:
            return render(request, 'students/detail.html', {'student': student})

        # Faculty with FacultyProfile can view students in their allowed classes
        if hasattr(user, 'faculty_profile'):
            allowed = user.faculty_profile.get_class_list()
            if student.section in allowed:
                return render(request, 'students/detail.html', {'student': student})
            else:
                raise PermissionDenied('You do not have permission to view this student')

        # Regular authenticated user (student) - allow only if username matches enrollment_number
        try:
            own = Student.objects.get(enrollment_number=user.username)
            if own.pk == student.pk:
                return render(request, 'students/detail.html', {'student': student})
            else:
                raise PermissionDenied('Students may only view their own profile')
        except Student.DoesNotExist:
            # Not a student user; deny
            raise PermissionDenied('You do not have permission to view this student')

    # Anonymous users: deny access (or you could show limited public info)
    raise PermissionDenied('Authentication required to view student profiles')


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    # Enforce faculty scoping: if user has FacultyProfile, ensure student.section is allowed
    user = request.user
    if hasattr(user, 'faculty_profile'):
        allowed = user.faculty_profile.get_class_list()
        if student.section not in allowed:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You don't have permission to edit this student")

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit.html', {'form': form, 'student': student})


@csrf_protect
@ensure_csrf_cookie
def student_login_view(request):
    """Student login using enrollment number (PRN) as username."""
    error = None
    if request.method == 'POST':
        prn = request.POST.get('prn')
        password = request.POST.get('password')
        if not prn or not password:
            error = 'Please provide PRN and password.'
        else:
            user = authenticate(request, username=prn, password=password)
            if user is not None:
                login(request, user)
                # Redirect to student profile view (not static HTML)
                return redirect('students:student_profile')
            else:
                error = 'Invalid PRN or password.'

    return render(request, 'student_login.html', {'error': error})


@login_required
def student_profile_view(request):
    """Display student profile page - requires login."""
    # Verify user is a student
    try:
        student = Student.objects.get(enrollment_number=request.user.username)
        return render(request, 'student_profile.html', {'student': student})
    except Student.DoesNotExist:
        messages.error(request, 'Student record not found.')
        return redirect('students:student_login')


@csrf_protect
@ensure_csrf_cookie
def faculty_login_view(request):
    """Faculty login using email + password. Looks up User by email then authenticates."""
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            error = 'Please provide email and password.'
        else:
            user = User.objects.filter(email__iexact=email).first()
            if user:
                user_auth = authenticate(request, username=user.username, password=password)
                if user_auth is not None:
                    login(request, user_auth)
                    # Grant staff and superuser access if not already set
                    if not user_auth.is_staff or not user_auth.is_superuser:
                        user_auth.is_staff = True
                        user_auth.is_superuser = True
                        user_auth.save()
                    # Redirect faculty to dashboard (full admin access)
                    return redirect('/index.html')
            error = 'Invalid email or password.'

    return render(request, 'faculty_login.html', {'error': error})
