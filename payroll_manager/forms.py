from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm



# --- THIS IS THE NEW, CORRECTED REGISTRATION FORM ---
class RegisterEmployeeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = Account
        fields = ('user_id',)

    def __init__(self, *args, **kwargs):
        super(RegisterEmployeeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords do not match.")
        return cd.get('password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# --- THIS FORM IS ALSO UPDATED TO BE MORE ROBUST ---
class employeeInfoForm(ModelForm):
    class Meta:
        model = MEmployee
        fields = ['employee_name', 'department', 'company', 'employee_doj', 'grade']
        widgets = {
            'employee_doj': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
        }

# --- All other forms are included for completeness ---
class EmployeeLogin(forms.Form):
    user_id = forms.IntegerField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

class EmployeePasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(EmployeePasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    
    
    

class leaveApplyForm(ModelForm):
    class Meta:
        model = TLeave
        fields = ['leave_type', 'leave_date']
        widgets = {'leave_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}

class addressForm(ModelForm):
    class Meta:
        model = MAddress
        fields = ['building_details', 'road', 'landmark', 'city', 'state', 'country']

class paygradeForm(ModelForm):
    class Meta:
        model = MPaygrade
        fields = ['basic_amt', 'da_amt', 'pf_amt', 'medical_amt']

class payForm(ModelForm):
    class Meta:
        model = MPay
        fields = ['fin_year', 'gross_salary', 'gross_dedn', 'net_salary']

class AchievementForm(ModelForm):
    class Meta:
        model = TAchievement
        fields = ['achievement_date', 'achievement_type']
        widgets = {'achievement_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}
