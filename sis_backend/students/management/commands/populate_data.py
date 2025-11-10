from django.core.management.base import BaseCommand
from students.models import Student, Attendance, Mark
from datetime import date, timedelta
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Populates the database with sample student data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Student.objects.all().delete()
        Attendance.objects.all().delete()
        Mark.objects.all().delete()
        
        self.stdout.write('Creating 130 sample students...')

        departments = ['Computer Science', 'IT', 'Electronics', 'Mechanical', 'Civil']
        class_years = ['B.Tech CSE - 3', 'B.Tech IT - 3', 'B.Tech ECE - 3', 'B.Tech MECH - 4']

        created_students = []
        # Generate 130 students with unique enrollment numbers
        for i in range(1, 131):
            enr = f'SIS2023{str(i).zfill(4)}'  # SIS20230001 .. SIS20230130
            firstname = f'Student{i}'
            lastname = 'Batch'
            dept = random.choice(departments)
            cls = random.choice(class_years)
            semester = random.randint(1, 8)
            dob = date(2002 + (i % 5), random.randint(1, 12), random.randint(1, 28))
            contact = f'+91 90000{str(1000 + i)}'
            addr = f'{i} College Road, City {i%10}, State'

            student = Student.objects.create(
                first_name=firstname,
                last_name=lastname,
                enrollment_number=enr,
                email=f'{firstname.lower()}@college.edu',
                class_year=cls,
                department=dept,
                semester=semester,
                # Assign a deterministic section value for seeded students
                section=(
                    'SY-COMP-A' if ('computer' in dept.lower() and semester in (3,4) and (i % 2 == 0)) else
                    'SY-COMP-B' if ('computer' in dept.lower() and semester in (3,4)) else
                    'TY-COMP-A' if ('computer' in dept.lower() and semester in (5,6) and (i % 2 == 0)) else
                    'TY-COMP-B' if ('computer' in dept.lower() and semester in (5,6)) else
                    f'UG-{dept.upper().replace(" ", "_")}-{(i%3)+1}'
                ),
                contact=contact,
                gender=random.choice(['Male', 'Female', 'Other']),
                date_of_birth=dob,
                address=addr
            )
            created_students.append(student)
            self.stdout.write(f'  ✓ Created: {student.first_name} {student.last_name} ({student.enrollment_number})')
        
        # Add sample attendance records for last 7 days
        self.stdout.write('\nAdding attendance records...')
        today = date.today()
        for i in range(7):
            attendance_date = today - timedelta(days=i)
            for student in created_students:
                # 90% attendance rate
                is_present = random.random() < 0.9
                Attendance.objects.create(
                    student=student,
                    date=attendance_date,
                    present=is_present
                )
        self.stdout.write(f'  ✓ Added attendance for last 7 days')
        
        # Add sample marks
        self.stdout.write('\nAdding marks...')
        subjects = [
            'Data Structures',
            'Database Management',
            'Operating Systems',
            'Web Development',
            'Computer Networks'
        ]
        
        for student in created_students:
            for subject in subjects:
                marks_obtained = random.randint(60, 95)
                Mark.objects.create(
                    student=student,
                    subject=subject,
                    marks_obtained=marks_obtained,
                    max_marks=100
                )
        self.stdout.write(f'  ✓ Added marks for {len(subjects)} subjects')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully populated database with {len(created_students)} students!'))
        # Ensure an admin user exists for login
        User = get_user_model()
        admin_username = 'admin'
        admin_password = 'admin123'
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(username=admin_username, email='admin@college.edu', password=admin_password)
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_username} / {admin_password}'))
        else:
            self.stdout.write(f'Admin user "{admin_username}" already exists')

        # Create groups and assign model permissions
        self.stdout.write('\nConfiguring role-based groups and permissions...')
        # content type for Student model
        ct = ContentType.objects.get_for_model(Student)

        # Define perms
        add_perm = Permission.objects.get(content_type=ct, codename='add_student')
        change_perm = Permission.objects.get(content_type=ct, codename='change_student')
        delete_perm = Permission.objects.get(content_type=ct, codename='delete_student')
        view_perm = Permission.objects.get(content_type=ct, codename='view_student')

        # Admin group: all student perms
        admin_group, created = Group.objects.get_or_create(name='Admin')
        admin_group.permissions.set([add_perm, change_perm, delete_perm, view_perm])
        admin_group.save()

        # Teacher group: view and change but not delete
        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        teacher_group.permissions.set([view_perm, change_perm])
        teacher_group.save()

        self.stdout.write('  ✓ Groups Admin and Teacher created/updated')

        # Create example teacher user
        teacher_username = 'teacher'
        teacher_password = 'teacher123'
        if not User.objects.filter(username=teacher_username).exists():
            teacher = User.objects.create_user(username=teacher_username, email='teacher@college.edu', password=teacher_password)
            teacher.groups.add(teacher_group)
            teacher.save()
            self.stdout.write(self.style.SUCCESS(f'Created teacher user: {teacher_username} / {teacher_password}'))
        else:
            self.stdout.write(f'Teacher user "{teacher_username}" already exists')

        # Create example faculty Bhushan with specific classes/subjects
        bh_username = 'bhushan'
        bh_password = 'bhushan123'
        if not User.objects.filter(username=bh_username).exists():
            bh = User.objects.create_user(username=bh_username, email='bhushan@example.com', password=bh_password, first_name='Bhushan', last_name='Sir')
            bh.groups.add(teacher_group)
            bh.save()
            # Create FacultyProfile if model is available
            try:
                from students.models import FacultyProfile
                FacultyProfile.objects.update_or_create(user=bh, defaults={
                    'subjects': 'Data Structures,DAA',
                    'classes': 'SY-COMP-A,SY-COMP-B,TY-COMP-A,TY-COMP-B'
                })
            except Exception:
                pass
            self.stdout.write(self.style.SUCCESS(f'Created faculty user: {bh_username} / {bh_password}'))
        else:
            self.stdout.write(f'Faculty user "{bh_username}" already exists')

        # Sample SQL Query
        self.stdout.write('\nSample Query: Fetching first 20 students')
        students = Student.objects.all()[:20]
        for student in students:
            self.stdout.write(f'  - {student.id}: {student.enrollment_number}, {student.first_name} {student.last_name}, {student.email}, {student.section}')
