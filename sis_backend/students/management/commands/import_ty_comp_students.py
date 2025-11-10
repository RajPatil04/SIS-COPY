from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student, Attendance, Mark
from datetime import date, timedelta


RAW = """
14002230001 GAURI.AGRAWAL01@svkmmumbai.onmicrosoft.com GAURI AGRAWAL
14002230002 VAISHNAVI.AGRAWAL02@svkmmumbai.onmicrosoft.com VAISHNAVI AGRAWAL
14002230003 AISHWARYA.AMRUTKAR03@svkmmumbai.onmicrosoft.com AISHWARYA AMRUTKAR
14002230004 SHLOK.ANGALE04@svkmmumbai.onmicrosoft.com SHLOK ANGALE
14002230005 ANUSHKA.APURVA05@svkmmumbai.onmicrosoft.com ANUSHKA APURVA
14002230006 MAYUR.BADGUJAR06@svkmmumbai.onmicrosoft.com MAYUR BADGUJAR
14002230007 SHUBHAM.BALDANIYA07@svkmmumbai.onmicrosoft.com SHUBHAM BALDANIYA
14002230008 ABDULLAH.BANDUKWALA08@svkmmumbai.onmicrosoft.com ABDULLAH BANDUKWALA
14002230009 NEHA.BEHARE09@svkmmumbai.onmicrosoft.com NEHA BEHARE
14002230010 NIPUN.BHADANE10@svkmmumbai.onmicrosoft.com NIPUN BHADANE
14002230011 PARTH.BHANDARI11@svkmmumbai.onmicrosoft.com PARTH BHANDARI
14002230012 MADHUR.BHANDARKAR12@svkmmumbai.onmicrosoft.com MADHUR BHANDARKAR
14002230013 BHUMIKA.BHINGARE13@svkmmumbai.onmicrosoft.com BHUMIKA BHINGARE
14002230014 PRERANA.BHOI14@svkmmumbai.onmicrosoft.com PRERANA BHOI
14002230015 GUNWANT.BORSE15@svkmmumbai.onmicrosoft.com GUNWANT BORSE
14002230016 KARTIKA.BORSE16@svkmmumbai.onmicrosoft.com KARTIKA BORSE
14002230017 KETAN.BORSE17@svkmmumbai.onmicrosoft.com KETAN BORSE
14002230018 GAURAV.CHAUDHARI18@svkmmumbai.onmicrosoft.com GAURAV CHAUDHARI
14002230019 HIMANSHU.CHAUDHARI19@svkmmumbai.onmicrosoft.com HIMANSHU CHAUDHARI
14002230020 SOHAM.CHAUDHARI20@svkmmumbai.onmicrosoft.com SOHAM CHAUDHARI
14002230021 TARUN.CHAUDHARI21@svkmmumbai.onmicrosoft.com TARUN CHAUDHARI
14002230022 VAIBHAV.CHAUDHARI22@svkmmumbai.onmicrosoft.com VAIBHAV CHAUDHARI
14002230023 MAYURI.CHAVAN23@svkmmumbai.onmicrosoft.com MAYURI CHAVAN
14002230024 PUSHKRAJ.CHAVHAN24@svkmmumbai.onmicrosoft.com PUSHKRAJ CHAVHAN
14002230025 TANMAY.CHITODKAR25@svkmmumbai.onmicrosoft.com TANMAY CHITODKAR
14002230026 MRUNAL.DEORE26@svkmmumbai.onmicrosoft.com MRUNAL DEORE
14002230027 MRUNALI.DESALE27@svkmmumbai.onmicrosoft.com MRUNALI DESALE
14002230028 VAISHNAVI.DESALE28@svkmmumbai.onmicrosoft.com VAISHNAVI DESALE
14002230029 YOGINI.DESALE29@svkmmumbai.onmicrosoft.com YOGINI DESALE
14002230030 BHAVESH.DEV30@svkmmumbai.onmicrosoft.com BHAVESH DEV
14002230031 ATHARV.DHAGE31@svkmmumbai.onmicrosoft.com ATHARV DHAGE
14002230032 UNNATI.FULPAGARE32@svkmmumbai.onmicrosoft.com UNNATI FULPAGARE
14002230033 KAVERI.GAWALI33@svkmmumbai.onmicrosoft.com KAVERI GAWALI
14002230034 PRIYANKA.GAWALI34@svkmmumbai.onmicrosoft.com PRIYANKA GAWALI
14002230035 SAURABH.GIRASE35@svkmmumbai.onmicrosoft.com SAURABH GIRASE
14002230036 VIJAY.GIRASE36@svkmmumbai.onmicrosoft.com VIJAY GIRASE
14002230037 CHETAN.GUJAR37@svkmmumbai.onmicrosoft.com CHETAN GUJAR
14002230038 AISHA.GUJARATHI38@svkmmumbai.onmicrosoft.com AISHA GUJARATHI
14002230039 BHUMI.GUJARATHI39@svkmmumbai.onmicrosoft.com BHUMI GUJARATHI
14002230040 PRATIKSHA.HATKAR40@svkmmumbai.onmicrosoft.com PRATIKSHA HATKAR
14002230041 TEJAS.HIRE41@svkmmumbai.onmicrosoft.com TEJAS HIRE
14002230042 PRADNYA.INDAVE42@svkmmumbai.onmicrosoft.com PRADNYA INDAVE
14002230043 AASHISH.INGALE43@svkmmumbai.onmicrosoft.com AASHISH INGALE
14002230044 ADITYA.JADE44@svkmmumbai.onmicrosoft.com ADITYA JADE
14002230045 DARSHAN.JADHAV45@svkmmumbai.onmicrosoft.com DARSHAN JADHAV
14002230046 MAYUR.JADHAV46@svkmmumbai.onmicrosoft.com MAYUR JADHAV
14002230047 PRAPTI.JAIN47@svkmmumbai.onmicrosoft.com PRAPTI JAIN
14002230048 GAYATRI.JANGID48@svkmmumbai.onmicrosoft.com GAYATRI JANGID
14002230049 ASHLESHA.JOSHI49@svkmmumbai.onmicrosoft.com ASHLESHA JOSHI
14002230050 BHAGYESH.JOSHI50@svkmmumbai.onmicrosoft.com BHAGYESH JOSHI
14002230051 LALIT.JOSHI51@svkmmumbai.onmicrosoft.com LALIT JOSHI
14002230052 MANALI.KHAIRNAR52@svkmmumbai.onmicrosoft.com MANALI KHAIRNAR
14002230053 PRANAY.KHAIRNAR53@svkmmumbai.onmicrosoft.com PRANAY KHAIRNAR
14002230054 SHIVAM.KHALANE54@svkmmumbai.onmicrosoft.com SHIVAM KHALANE
14002230055 MAYUR.KOLEKAR55@svkmmumbai.onmicrosoft.com MAYUR KOLEKAR
14002230056 CHETAN.KOLI56@svkmmumbai.onmicrosoft.com CHETAN KOLI
14002230057 SANIKA.KULKARNI57@svkmmumbai.onmicrosoft.com SANIKA KULKARNI
14002230058 VAIBHAV.KULKARNI58@svkmmumbai.onmicrosoft.com VAIBHAV KULKARNI
14002230059 RAJESHWARI.MAHALE59@svkmmumbai.onmicrosoft.com RAJESHWARI MAHALE
14002230060 JAYESH.MALI60@svkmmumbai.onmicrosoft.com JAYESH MALI
14002230061 PREM.MALI61@svkmmumbai.onmicrosoft.com PREM MALI
14002230062 TRUPTI.MALI62@svkmmumbai.onmicrosoft.com TRUPTI MALI
14002230063 AMIT.MARATHE63@svkmmumbai.onmicrosoft.com AMIT MARATHE
14002230064 PIYUSH.MARATHE64@svkmmumbai.onmicrosoft.com PIYUSH MARATHE
14002230065 PRASAD.NERKAR65@svkmmumbai.onmicrosoft.com PRASAD NERKAR
14002230066 RUTUJA.NIMBALKAR66@svkmmumbai.onmicrosoft.com RUTUJA NIMBALKAR
14002230067 VAISHNAVI.PACHPUTE67@svkmmumbai.onmicrosoft.com VAISHNAVI PACHPUTE
14002230068 TEJAS.PARDESHI68@svkmmumbai.onmicrosoft.com TEJAS PARDESHI
14002230069 SMEET.PATEL69@svkmmumbai.onmicrosoft.com SMEET PATEL
14002230070 ARYAN.PATIL70@svkmmumbai.onmicrosoft.com ARYAN PATIL
14002230071 BHAVESH.PATIL71@svkmmumbai.onmicrosoft.com BHAVESH PATIL
14002230072 DEVENDRA.PATIL72@svkmmumbai.onmicrosoft.com DEVENDRA PATIL
14002230073 DHANASHRI.PATIL73@svkmmumbai.onmicrosoft.com DHANASHRI PATIL
14002230074 DHANASHRI.PATIL74@svkmmumbai.onmicrosoft.com DHANASHRI PATIL
14002230075 DHANASHRI.PATIL75@svkmmumbai.onmicrosoft.com DHANASHRI PATIL
14002230076 HEMANGI.PATIL76@svkmmumbai.onmicrosoft.com HEMANGI PATIL
14002230077 KALPESH.PATIL77@svkmmumbai.onmicrosoft.com KALPESH PATIL
14002230078 KALYANI.PATIL78@svkmmumbai.onmicrosoft.com KALYANI PATIL
14002230079 MANASI.PATIL79@svkmmumbai.onmicrosoft.com MANASI PATIL
14002230080 MANSI.PATIL80@svkmmumbai.onmicrosoft.com MANSI PATIL
14002230081 MANSWI.PATIL81@svkmmumbai.onmicrosoft.com MANSWI PATIL
14002230082 PAVAN.PATIL82@svkmmumbai.onmicrosoft.com PAVAN PATIL
14002230083 PIYUSHA.PATIL83@svkmmumbai.onmicrosoft.com PIYUSHA PATIL
14002230084 POOJA.PATIL84@svkmmumbai.onmicrosoft.com POOJA PATIL
14002230085 PRANAV.PATIL85@svkmmumbai.onmicrosoft.com PRANAV PATIL
14002230086 PRATIKSHA.PATIL86@svkmmumbai.onmicrosoft.com PRATIKSHA PATIL
14002230087 RAJSHRI.PATIL87@svkmmumbai.onmicrosoft.com RAJSHRI PATIL
14002230088 RAKSHA.PATIL88@svkmmumbai.onmicrosoft.com RAKSHA PATIL
14002230089 SHUBHANGI.PATIL89@svkmmumbai.onmicrosoft.com SHUBHANGI PATIL
14002230090 VIVEK.PATIL90@svkmmumbai.onmicrosoft.com VIVEK PATIL
14002230091 YASH.PATIL91@svkmmumbai.onmicrosoft.com YASH PATIL
14002230092 YOGESHWAR.PATIL92@svkmmumbai.onmicrosoft.com YOGESHWAR PATIL
14002230093 SUSHANT.PAWAR93@svkmmumbai.onmicrosoft.com SUSHANT PAWAR
14002230094 AMRUTA.POTDAR94@svkmmumbai.onmicrosoft.com AMRUTA POTDAR
14002230095 KAVERI.RAJPUT95@svkmmumbai.onmicrosoft.com KAVERI RAJPUT
14002230096 JAY.RAMANI96@svkmmumbai.onmicrosoft.com JAY RAMANI
14002230097 SHRUTI.RANMALE97@svkmmumbai.onmicrosoft.com SHRUTI RANMALE
14002230098 PURVA.SALUNKHE98@svkmmumbai.onmicrosoft.com PURVA SALUNKHE
14002230099 CHETAN.SAWANT99@svkmmumbai.onmicrosoft.com CHETAN SAWANT
14002230100 EHETESHAM.SHAIKH00@svkmmumbai.onmicrosoft.com EHETESHAM SHAIKH
14002230101 NITIN.SHINDE01@svkmmumbai.onmicrosoft.com NITIN SHINDE
14002230102 PRAVIN.SHINDE02@svkmmumbai.onmicrosoft.com PRAVIN SHINDE
14002230103 SAHIL.SHINDE03@svkmmumbai.onmicrosoft.com SAHIL SHINDE
14002230104 SUSHANT.SHINDE04@svkmmumbai.onmicrosoft.com SUSHANT SHINDE
14002230105 YOGIRAJ.SHINDE05@svkmmumbai.onmicrosoft.com YOGIRAJ SHINDE
14002230106 MITTAL.SHISODE06@svkmmumbai.onmicrosoft.com MITTAL SHISODE
14002230107 BHUMIKA.SONAWANE07@svkmmumbai.onmicrosoft.com BHUMIKA SONAWANE
14002230108 DURGESH.SONAWANE08@svkmmumbai.onmicrosoft.com DURGESH SONAWANE
14002230109 RUSHIKESH.SONAWANE09@svkmmumbai.onmicrosoft.com RUSHIKESH SONAWANE
14002230110 SARTHAK.SONAWANE10@svkmmumbai.onmicrosoft.com SARTHAK SONAWANE
14002230111 SAHIL.SONGIRKAR11@svkmmumbai.onmicrosoft.com SAHIL SONGIRKAR
14002230112 GAURAV.SONUNE12@svkmmumbai.onmicrosoft.com GAURAV SONUNE
14002230113 HARSHALA.SURYAWANSHI13@svkmmumbai.onmicrosoft.com HARSHALA SURYAWANSHI
14002230114 KAVERI.SURYAWANSHI14@svkmmumbai.onmicrosoft.com KAVERI SURYAWANSHI
14002230115 SHRUTI.TAMBAT15@svkmmumbai.onmicrosoft.com SHRUTI TAMBAT
14002230116 MANISH.THAKARE16@svkmmumbai.onmicrosoft.com MANISH THAKARE
14002230117 MANISH.VISPUTE17@svkmmumbai.onmicrosoft.com MANISH VISPUTE
14002230118 KAUSTUBH.YEOLEKAR18@svkmmumbai.onmicrosoft.com KAUSTUBH YEOLEKAR
14002230119 DIVYA.BADGUJAR19@svkmmumbai.onmicrosoft.com DIVYA BADGUJAR
14002230120 HARSHAL.PATEL20@svkmmumbai.onmicrosoft.com HARSHAL PATEL
14002230121 DIPTI.PATIL21@svkmmumbai.onmicrosoft.com DIPTI PATIL
14002230122 RAJ.PATIL22@svkmmumbai.onmicrosoft.com RAJ PATIL
14002230123 ROSHNI.PATIL23@svkmmumbai.onmicrosoft.com ROSHNI PATIL
14002230124 KANISHKA.WANI24@svkmmumbai.onmicrosoft.com KANISHKA WANI
"""


class Command(BaseCommand):
    help = 'Import TY Computer students from the provided list and replace existing students.'

    def handle(self, *args, **options):
        # Remove existing students and related records
        self.stdout.write('Clearing existing Student, Attendance and Mark data...')
        Attendance.objects.all().delete()
        Mark.objects.all().delete()
        Student.objects.all().delete()

        User = get_user_model()

        lines = [l.strip() for l in RAW.splitlines() if l.strip()]
        created = 0
        for i, line in enumerate(lines):
            parts = line.split()
            if len(parts) < 4:
                continue
            sap = parts[0].strip()
            email = parts[1].strip()
            first = parts[2].strip()
            last = parts[3].strip()

            section = 'TY-COMP-A' if (i % 2 == 0) else 'TY-COMP-B'
            student = Student.objects.create(
                first_name=first,
                last_name=last,
                enrollment_number=sap,
                email=email,
                class_year='TY Computer',
                department='Computer Science',
                semester=5,
                section=section,
            )
            created += 1

            # create Django user for student
            user, was_created = User.objects.get_or_create(username=sap, defaults={'email': email, 'first_name': first, 'last_name': last})
            if was_created:
                user.set_password('student123')
                user.save()

        self.stdout.write(self.style.SUCCESS(f'Imported {created} TY Computer students and created user accounts (password=student123)'))
