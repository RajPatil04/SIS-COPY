from django.contrib import admin
from .models import Student, Attendance, Mark

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'enrollment_number', 'email', 'class_year', 'department')
    search_fields = ('first_name', 'last_name', 'enrollment_number', 'class_year')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present')
    list_filter = ('present',)


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'max_marks')
    search_fields = ('student__first_name', 'student__last_name', 'subject')
