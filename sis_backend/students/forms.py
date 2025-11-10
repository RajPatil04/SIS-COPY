from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'enrollment_number', 'email', 'date_of_birth',
            'class_year', 'department', 'semester', 'contact', 'address', 'gender'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
