from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('Users must have a userID')

        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_employer', True)
        extra_fields.setdefault('is_employee', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, password, **extra_fields)


class Account(AbstractBaseUser):
    user_id = models.IntegerField(verbose_name="user_id", unique=True, primary_key=True)
    is_employer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True, verbose_name='email')
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    def __str__(self):
        return str(self.user_id)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class MState(models.Model):
    state_code = models.CharField(primary_key=True, max_length=2)
    state_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'm_state'
    def __str__(self):
        return self.state_name + ' (' + self.state_code + ')'


class MAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    # FIX Part 1: Explicitly name the reverse relationship from MEmployee to MAddress
    memployee = models.ForeignKey('MEmployee', on_delete=models.CASCADE, null=True, blank=True, related_name='employee_addresses')
    building_details = models.CharField(max_length=30)
    road = models.CharField(max_length=20)
    landmark = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.ForeignKey('MState', on_delete=models.CASCADE)
    country = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'm_address'
    def __str__(self):
        return str(self.address_id)+ ' ' + self.building_details


class MCompany(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=50)
    address = models.ForeignKey('MAddress',on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'm_company'
    def __str__(self):
        return self.company_name


class MDepartment(models.Model):
    company = models.ForeignKey('MCompany',on_delete=models.CASCADE)
    department_id = models.IntegerField(primary_key=True)
    department_name = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'm_department'
    def __str__(self):
        return self.department_name


class MGrade(models.Model):
    grade_id = models.IntegerField(primary_key=True)
    grade_name = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'm_grade'
    def __str__(self):
        return self.grade_name


class MEmployee(models.Model):
    employee = models.OneToOneField('Account',primary_key=True,on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=30)
    department = models.ForeignKey('MDepartment',on_delete=models.CASCADE)
    company = models.ForeignKey('MCompany',on_delete=models.CASCADE)
    # FIX Part 2: Explicitly name the reverse relationship from MAddress to MEmployee
    address = models.ForeignKey('MAddress',on_delete=models.CASCADE, blank=True, null=True, related_name='address_for_employee')
    employee_doj = models.DateField()
    grade = models.ForeignKey('MGrade',on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'm_employee'


class MPaygrade(models.Model):
    employee = models.ForeignKey('MEmployee',on_delete=models.CASCADE)
    grade = models.ForeignKey('MGrade',on_delete=models.CASCADE)
    basic_amt = models.IntegerField()
    da_amt = models.IntegerField()
    pf_amt = models.IntegerField()
    medical_amt = models.IntegerField()
    paygrade_id = models.AutoField(primary_key=True)
    class Meta:
        managed = True
        db_table = 'm_paygrade'
        unique_together = (('employee', 'grade'),)


class MPay(models.Model):
    employee = models.ForeignKey('MEmployee',on_delete=models.CASCADE)
    fin_year = models.IntegerField()
    gross_salary = models.IntegerField()
    gross_dedn = models.IntegerField()
    net_salary = models.IntegerField()
    MPay_id = models.AutoField(primary_key=True)
    class Meta:
        managed = True
        db_table = 'm_pay'
        unique_together = (('fin_year', 'employee'),)


class TLeave(models.Model):
    employee = models.ForeignKey('MEmployee',on_delete=models.CASCADE)
    fin_year = models.IntegerField()
    leave_date = models.DateField()
    leave_choices = [
        ('CL', 'CL'),
        ('SL', 'SL'),
        ('PL', 'PL'),
        ('LWP', 'LWP'),
    ]
    leave_type= models.CharField(max_length=4, choices=leave_choices)
    is_approved = models.IntegerField(default=0, validators=[MaxValueValidator(1), MinValueValidator(-1)])
    leave_id =models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 't_leave'


class TAchievement(models.Model):
    employee = models.ForeignKey('MEmployee',on_delete=models.CASCADE)
    achievement_date = models.DateField()
    achievement_type = models.CharField(max_length=80)
    achievement_id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        db_table = 't_achievement'

