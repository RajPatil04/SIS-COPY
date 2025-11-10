from rest_framework import serializers
from .models import Student, Attendance, Mark


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'email', 'enrollment_number', 'date_of_birth',
            'class_year', 'department', 'semester', 'section', 'contact', 'address', 'gender'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'date', 'present']


class MarkSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'marks_obtained', 'max_marks']
