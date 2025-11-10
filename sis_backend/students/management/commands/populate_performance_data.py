from django.core.management.base import BaseCommand
from students.models import Student, Attendance, Mark
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate attendance and marks data for performance analytics'

    def handle(self, *args, **options):
        self.stdout.write('Populating attendance and marks data...\n')
        
        # Get all students
        students = Student.objects.all()
        
        if not students.exists():
            self.stdout.write(self.style.ERROR('No students found. Run populate_data first.'))
            return
        
        # Clear existing data
        Attendance.objects.all().delete()
        Mark.objects.all().delete()
        
        # Generate attendance for the last 6 days (Mon-Sat)
        today = datetime.now().date()
        days_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        
        attendance_count = 0
        marks_count = 0
        
        # Performance variations by year and division
        performance_config = {
            'FY Computer - A': {'attendance': 88, 'marks': 82},
            'FY Computer - B': {'attendance': 90, 'marks': 84},
            'FY Computer - C': {'attendance': 86, 'marks': 80},
            'SY Computer - A': {'attendance': 92, 'marks': 85},
            'SY Computer - B': {'attendance': 90, 'marks': 83},
            'SY Computer - C': {'attendance': 88, 'marks': 81},
            'TY Computer - A': {'attendance': 94, 'marks': 88},
            'TY Computer - B': {'attendance': 92, 'marks': 86},
            'TY Computer - C': {'attendance': 90, 'marks': 84},
        }
        
        for student in students:
            # Get base performance for student's class
            class_key = student.class_year
            config = performance_config.get(class_key, {'attendance': 85, 'marks': 80})
            
            # Generate attendance for last 6 days
            for i in range(6):
                date = today - timedelta(days=5-i)
                # Random variation around base attendance rate
                base_rate = config['attendance']
                is_present = random.randint(1, 100) <= base_rate + random.randint(-3, 3)
                
                Attendance.objects.create(
                    student=student,
                    date=date,
                    present=is_present
                )
                attendance_count += 1
            
            # Generate marks for subjects
            subjects = ['Data Structures', 'Database Management', 'Operating Systems', 
                       'Computer Networks', 'Software Engineering']
            
            for subject in subjects:
                base_marks = config['marks']
                # Random variation around base marks
                marks = max(0, min(100, base_marks + random.randint(-5, 5)))
                
                Mark.objects.create(
                    student=student,
                    subject=subject,
                    marks_obtained=marks,
                    max_marks=100
                )
                marks_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Created {attendance_count} attendance records'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Created {marks_count} marks records'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Performance data populated successfully!'
            )
        )
