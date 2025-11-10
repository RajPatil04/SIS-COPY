from django.core.management.base import BaseCommand
from students.models import Student


class Command(BaseCommand):
    help = 'Display all student login credentials'

    def handle(self, *args, **options):
        students = Student.objects.all().order_by('enrollment_number')
        
        print('=' * 75)
        print('STUDENT LOGIN CREDENTIALS'.center(75))
        print('=' * 75)
        print(f'\nTotal Students: {students.count()}\n')
        print(f'{"SAP ID":<20} {"Name":<35} {"Section":<15}')
        print('-' * 75)
        
        for s in students:
            name = f"{s.first_name} {s.last_name}"
            print(f'{s.enrollment_number:<20} {name:<35} {s.section or "N/A":<15}')
        
        print('-' * 75)
        print('\n✓ Password for ALL students: student123')
        print('✓ Each student logs in with their unique SAP ID')
        print('✓ Example Login:')
        print('  - SAP ID: 14002230001')
        print('  - Password: student123')
        print('\n✓ Login URL: http://127.0.0.1:8000/students/login/')
        print('=' * 75)
        
        self.stdout.write(self.style.SUCCESS('\nStudent credentials displayed successfully!'))
