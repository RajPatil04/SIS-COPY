from django.core.management.base import BaseCommand
from students.models import Student


class Command(BaseCommand):
    help = 'Assigns a plausible `section` value to students based on department and semester heuristics.'

    def handle(self, *args, **options):
        students = Student.objects.all()
        updated = 0
        for i, s in enumerate(students):
            if s.section:
                continue

            dept = (s.department or '').lower()
            sem = s.semester or 1

            # Basic heuristics for Computer dept
            if 'computer' in dept or 'cse' in dept or 'comp' in dept:
                if sem in (3, 4):
                    # Second year - SY
                    section = 'SY-COMP-A' if (i % 2 == 0) else 'SY-COMP-B'
                elif sem in (5, 6):
                    # Third year - TY
                    section = 'TY-COMP-A' if (i % 2 == 0) else 'TY-COMP-B'
                else:
                    section = f'UG-COMP-{(i%3)+1}'
            else:
                # Generic section: YEAR-DEPT-X
                year = 'UG'
                section = f'{year}-{(s.department or "GEN").upper().replace(" ", "_")}-{(i%3)+1}'

            s.section = section
            s.save()
            updated += 1

        self.stdout.write(self.style.SUCCESS(f'Assigned section to {updated} students'))
