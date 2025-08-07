# In payroll_manager/management/commands/seed_database.py

from django.core.management.base import BaseCommand
from datetime import date

# Import all your models directly
from payroll_manager.models import (
    MState, MAddress, MCompany, MDepartment, MGrade, Account,
    MEmployee, MPaygrade, MPay, TLeave, TAchievement
)

class Command(BaseCommand):
    help = 'Deletes old data and seeds the database with the specific data from the SQL script.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('[Seed] Starting database refresh...'))

        # --- Deleting Old Data ---
        self.stdout.write(self.style.WARNING('--> Deleting old records...'))
        TAchievement.objects.all().delete()
        TLeave.objects.all().delete()
        MPay.objects.all().delete()
        MPaygrade.objects.all().delete()
        MEmployee.objects.all().delete()

        all_users = Account.objects.all()
        deleted_count = 0
        for user in all_users:
            if not user.is_superuser:
                user.delete()
                deleted_count += 1
        self.stdout.write(self.style.WARNING(f'--> Deleted {deleted_count} non-admin user accounts.'))

        MDepartment.objects.all().delete()
        MCompany.objects.all().delete()
        MAddress.objects.all().delete()
        MState.objects.all().delete()
        MGrade.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('--> Old data deleted successfully.'))

        # --- Creating New Data ---
        self.stdout.write(self.style.SUCCESS('[Seed] Populating database with new data...'))

        # States
        MState.objects.get_or_create(state_code='TN', defaults={'state_name': 'Tamil Nadu'})
        MState.objects.get_or_create(state_code='WB', defaults={'state_name': 'West Bengal'})
        MState.objects.get_or_create(state_code='MP', defaults={'state_name': 'Madhya Pradesh'})
        MState.objects.get_or_create(state_code='UP', defaults={'state_name': 'Uttar Pradesh'})
        MState.objects.get_or_create(state_code='RA', defaults={'state_name': 'Rajasthan'})
        
        # Addresses
        state_tn = MState.objects.get(state_code='TN')
        state_wb = MState.objects.get(state_code='WB')
        state_mp = MState.objects.get(state_code='MP')
        state_up = MState.objects.get(state_code='UP')
        state_ra = MState.objects.get(state_code='RA')

        addr_101, _ = MAddress.objects.get_or_create(address_id=101, defaults={'building_details': 'Buil-A', 'road': '5th Road', 'landmark': 'Near City Mall', 'city': 'Kolkata', 'state': state_wb, 'country': 'India'})
        addr_102, _ = MAddress.objects.get_or_create(address_id=102, defaults={'building_details': 'Sun Buil', 'road': 'Beena Road', 'landmark': 'Near MeenaBazaar', 'city': 'Bareily', 'state': state_up, 'country': 'India'})
        addr_103, _ = MAddress.objects.get_or_create(address_id=103, defaults={'building_details': 'Coach Buil', 'road': 'Nani Road', 'landmark': 'Near Cine Hall', 'city': 'Jaipur', 'state': state_ra, 'country': 'India'})
        addr_104, _ = MAddress.objects.get_or_create(address_id=104, defaults={'building_details': 'Farmer Buil', 'road': 'Rajesh Road', 'landmark': 'Near Vellore Fort', 'city': 'Vellore', 'state': state_tn, 'country': 'India'})
        addr_105, _ = MAddress.objects.get_or_create(address_id=105, defaults={'building_details': 'Buil-X', 'road': 'Nano Road', 'landmark': 'Near MaxStore', 'city': 'Bhopal', 'state': state_mp, 'country': 'India'})
        addr_106, _ = MAddress.objects.get_or_create(address_id=106, defaults={'building_details': 'Office Buil', 'road': 'Nicco Park', 'landmark': 'Near SaltLake', 'city': 'Kolkata', 'state': state_wb, 'country': 'India'})

        # Companies
        comp_1, _ = MCompany.objects.get_or_create(company_id=1, defaults={'company_name': 'InfoBliss Capital', 'address': addr_101})
        comp_2, _ = MCompany.objects.get_or_create(company_id=2, defaults={'company_name': 'InfoBliss Cloud Solutions', 'address': addr_103})
        comp_3, _ = MCompany.objects.get_or_create(company_id=3, defaults={'company_name': 'InfoBliss Aegis', 'address': addr_104})

        # Departments
        dept_11, _ = MDepartment.objects.get_or_create(department_id=11, company=comp_1, defaults={'department_name': 'Human Resources'})
        dept_12, _ = MDepartment.objects.get_or_create(department_id=12, company=comp_2, defaults={'department_name': 'Human Resources'})
        dept_13, _ = MDepartment.objects.get_or_create(department_id=13, company=comp_1, defaults={'department_name': 'Marketing'})
        dept_14, _ = MDepartment.objects.get_or_create(department_id=14, company=comp_2, defaults={'department_name': 'Technical'})
        dept_15, _ = MDepartment.objects.get_or_create(department_id=15, company=comp_3, defaults={'department_name': 'Accounts & Finance'})
        dept_16, _ = MDepartment.objects.get_or_create(department_id=16, company=comp_3, defaults={'department_name': 'Production'})
        dept_17, _ = MDepartment.objects.get_or_create(department_id=17, company=comp_2, defaults={'department_name': 'Research & Development'})
        dept_18, _ = MDepartment.objects.get_or_create(department_id=18, company=comp_1, defaults={'department_name': 'Accounts & Finance'})
        
        # Grades
        grade_1, _ = MGrade.objects.get_or_create(grade_id=1, defaults={'grade_name': 'Head of Department'})
        grade_2, _ = MGrade.objects.get_or_create(grade_id=2, defaults={'grade_name': 'Senior Officer'})
        grade_3, _ = MGrade.objects.get_or_create(grade_id=3, defaults={'grade_name': 'Junior Staff'})
        grade_4, _ = MGrade.objects.get_or_create(grade_id=4, defaults={'grade_name': 'Janitor'})

        # Create Admin User
        if not Account.objects.filter(user_id=999).exists():
            Account.objects.create_superuser(user_id=999, password='adminpassword')
            self.stdout.write(self.style.SUCCESS("--> Admin user '999' created."))

        # Create Employees, Accounts, Pay, etc.
        employees_data = [
            {'uid': 1, 'name': 'Rajesh Raushan', 'pass': 'rajesh123', 'dept': dept_11, 'comp': comp_1, 'addr': addr_102, 'doj': '2015-02-01', 'grade': grade_1},
            {'uid': 2, 'name': 'Vinay Verma', 'pass': 'vinay123', 'dept': dept_12, 'comp': comp_2, 'addr': addr_104, 'doj': '2014-09-12', 'grade': grade_1},
            {'uid': 3, 'name': 'Divya Doijod', 'pass': 'divya123', 'dept': dept_13, 'comp': comp_1, 'addr': addr_106, 'doj': '2019-12-01', 'grade': grade_2},
            {'uid': 4, 'name': 'Manisha Mangal', 'pass': 'manisha123', 'dept': dept_14, 'comp': comp_2, 'addr': addr_105, 'doj': '2018-08-30', 'grade': grade_2},
            {'uid': 5, 'name': 'Payal Pandey', 'pass': 'payal123', 'dept': dept_15, 'comp': comp_3, 'addr': addr_101, 'doj': '2018-05-23', 'grade': grade_1},
            {'uid': 6, 'name': 'Nandana Nair', 'pass': 'nandana123', 'dept': dept_16, 'comp': comp_3, 'addr': addr_104, 'doj': '2017-09-15', 'grade': grade_2},
            {'uid': 7, 'name': 'Anant Agarwal', 'pass': 'anant123', 'dept': dept_17, 'comp': comp_2, 'addr': addr_105, 'doj': '2020-04-11', 'grade': grade_3},
            {'uid': 8, 'name': 'Kanan Kapoor', 'pass': 'kanan123', 'dept': dept_18, 'comp': comp_1, 'addr': addr_102, 'doj': '2019-07-10', 'grade': grade_3},
            {'uid': 9, 'name': 'Tanmay Tandon', 'pass': 'tanmay123', 'dept': dept_15, 'comp': comp_3, 'addr': addr_102, 'doj': '2017-05-28', 'grade': grade_3},
            {'uid': 10, 'name': 'Farah Fisher', 'pass': 'farah123', 'dept': dept_11, 'comp': comp_1, 'addr': addr_103, 'doj': '2018-11-19', 'grade': grade_3},
            {'uid': 11, 'name': 'Howard Herman', 'pass': 'howard123', 'dept': dept_15, 'comp': comp_3, 'addr': addr_106, 'doj': '1995-08-25', 'grade': grade_4},
        ]

        for emp in employees_data:
            if not Account.objects.filter(user_id=emp['uid']).exists():
                # --- THIS IS THE CORRECTED LINE ---
                user = Account.objects.create_user(user_id=emp['uid'], password=emp['pass'], is_employee=True)
                MEmployee.objects.create(
                    employee=user, employee_name=emp['name'], department=emp['dept'], company=emp['comp'], 
                    address=emp['addr'], employee_doj=emp['doj'], grade=emp['grade']
                )
        self.stdout.write(self.style.SUCCESS(f'--> All employee accounts created.'))

        self.stdout.write(self.style.SUCCESS('\n[Seed] Database population complete.'))
