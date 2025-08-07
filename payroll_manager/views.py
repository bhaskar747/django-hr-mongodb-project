from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash

# --- Login & Index Views ---

def index(request):
    return render(request, 'payroll_manager/index.html')

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST.get('user_id')
        p = request.POST.get('password')
        user = authenticate(request, user_id=u, password=p)
        if user is not None and user.is_employer:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid credentials or you are not an admin."
    return render(request, 'payroll_manager/admin_login.html', {'error': error})

def employee_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST.get('user_id')
        p = request.POST.get('password')
        user = authenticate(request, user_id=u, password=p)
        if user is not None and user.is_employee:
            login(request, user)
            return redirect('employee_dashboard', emp_id=user.user_id)
        else:
            error = "Invalid credentials or you are not an employee."
    form = EmployeeLogin()
    return render(request, 'payroll_manager/employee_login.html', {'form': form, 'error': error})

# --- Dashboard Views ---

@login_required
def admin_dashboard(request):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to access that page.')
        return redirect('index')
    
    allEmp = MEmployee.objects.all()
    LeaveRequests = TLeave.objects.filter(is_approved=0)
    context = {'allEmp': allEmp, 'LeaveR': LeaveRequests}
    return render(request, 'payroll_manager/admin_dashboard.html', context)

@login_required
def employee_dashboard(request, emp_id):
    if request.user.user_id != int(emp_id):
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('index')

    user_info = MEmployee.objects.filter(employee=request.user).first()
    context = {
        'user_info': user_info,
        'user_paygrade': MPaygrade.objects.filter(employee=user_info).first() if user_info else None,
        'user_pay': MPay.objects.filter(employee=user_info).first() if user_info else None,
        'user_achieve': TAchievement.objects.filter(employee=user_info) if user_info else None,
        'user_leave': TLeave.objects.filter(employee=user_info) if user_info else None
    }
    return render(request, 'payroll_manager/employee_dashboard.html', context)

def change_password(request):
    if request.method == 'POST':
        form = EmployeePasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('employee_dashboard', emp_id=request.user.user_id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EmployeePasswordChangeForm(request.user)
    return render(request, 'payroll_manager/change_password.html', {'form': form})

@login_required
def admin_employee_dashboard(request, emp_id):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to access that page.')
        return redirect('index')

    user = get_object_or_404(Account, user_id=emp_id)
    user_info = MEmployee.objects.filter(employee=user).first()
    context = {
        'user_info': user_info,
        'user_paygrade': MPaygrade.objects.filter(employee=user_info).first() if user_info else None,
        'user_pay': MPay.objects.filter(employee=user_info).first() if user_info else None,
        'user_achieve': TAchievement.objects.filter(employee=user_info) if user_info else None,
        'user_leave': TLeave.objects.filter(employee=user_info) if user_info else None
    }
    return render(request, 'payroll_manager/admin_employee_dashboard.html', context)

# --- Employee/Admin Actions ---

@login_required
@login_required
# In payroll_manager/views.py

@login_required
def register(request):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = RegisterEmployeeForm(request.POST)
        formSub = employeeInfoForm(request.POST)
        if form.is_valid() and formSub.is_valid():
            # Get the temporary password before it's hashed
            temp_password = form.cleaned_data.get('password')

            # First, save the account to get a user object
            user = form.save(commit=False)
            user.is_employee = True
            user.is_employer = False
            user.save()

            # Now, create the employee profile and link it to the user
            emp_info = formSub.save(commit=False)
            emp_info.employee = user
            emp_info.save()

            # UPDATED: The success message now includes the temporary password.
            messages.success(
                request, 
                f"Employee {user.user_id} created successfully. "
                f"Their temporary password is: {temp_password}. "
                f"Please instruct them to change it immediately."
            )
            return redirect('admin_dashboard')
    else:
        form = RegisterEmployeeForm()
        formSub = employeeInfoForm()
    
    context = {'form': form, 'formSub': formSub}
    return render(request, 'payroll_manager/register.html', context)



# --- ALL MISSING FUNCTIONS RESTORED AND SECURED ---

@login_required
def changeAddress(request, emp_id):
    user = get_object_or_404(Account, user_id=emp_id)
    employee_info = get_object_or_404(MEmployee, employee=user)

    # Authorization Check
    if not request.user.is_employer and request.user != user:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')

    address_instance, _ = MAddress.objects.get_or_create(memployee=employee_info)

    if request.method == 'POST':
        form = addressForm(request.POST, instance=address_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address Details Updated.')
            return redirect('admin_dashboard') if request.user.is_employer else redirect('employee_dashboard', emp_id=emp_id)
    else:
        form = addressForm(instance=address_instance)
    return render(request, 'payroll_manager/addressChange.html', {'form': form})

@login_required
def changePay(request, emp_id):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')

    user = get_object_or_404(Account, user_id=emp_id)
    employee_info = get_object_or_404(MEmployee, employee=user)
    
    pay_instance, _ = MPay.objects.get_or_create(employee=employee_info)
    paygrade_instance, _ = MPaygrade.objects.get_or_create(employee=employee_info)

    if request.method == 'POST':
        formPay = payForm(request.POST, instance=pay_instance)
        formPaygrade = paygradeForm(request.POST, instance=paygrade_instance)
        if formPay.is_valid() and formPaygrade.is_valid():
            formPay.save()
            formPaygrade.save()
            messages.success(request, 'Income Details Updated.')
            return redirect('admin_dashboard')
    else:
        formPay = payForm(instance=pay_instance)
        formPaygrade = paygradeForm(instance=paygrade_instance)
    context = {'formPay': formPay, 'formPaygrade': formPaygrade}
    return render(request, 'payroll_manager/payChange.html', context)

@login_required
def changeInfo(request, emp_id):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')
    
    user = get_object_or_404(Account, user_id=emp_id)
    employee_instance = get_object_or_404(MEmployee, employee=user)

    if request.method == 'POST':
        form = employeeInfoForm(request.POST, instance=employee_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal Details Updated.')
            return redirect('admin_dashboard')
    else:
        form = employeeInfoForm(instance=employee_instance)
    return render(request, 'payroll_manager/infoChange.html', {'form': form})

@login_required
def changeAchievement(request, emp_id):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')

    user = get_object_or_404(Account, user_id=emp_id)
    employee_info = get_object_or_404(MEmployee, employee=user)

    if request.method == 'POST':
        form = AchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.employee = employee_info
            achievement.save()
            messages.success(request, 'Achievement added.')
            return redirect('admin_dashboard')
    else:
        form = AchievementForm()
    return render(request, 'payroll_manager/achievementChange.html', {'form': form})

@login_required
def leaveApply(request, emp_id):
    if request.user.user_id != int(emp_id):
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')

    if request.method == 'POST':
        form = leaveApplyForm(request.POST)
        if form.is_valid():
            leave_app = form.save(commit=False)
            leave_app.employee = MEmployee.objects.get(employee=request.user)
            leave_app.fin_year = datetime.datetime.now().year
            leave_app.save()
            messages.success(request, 'Leave Application Submitted.')
            return redirect('employee_dashboard', emp_id=emp_id)
    else:
        form = leaveApplyForm()
    return render(request, 'payroll_manager/leaveApply.html', {'form': form})

@login_required
def approval(request, leave_id, app_id):
    if not request.user.is_employer:
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('admin_dashboard')

    leave = get_object_or_404(TLeave, leave_id=leave_id)
    if app_id == 1:
        leave.is_approved = 1
        messages.success(request, 'Leave request approved.')
    else:
        leave.is_approved = -1
        messages.warning(request, 'Leave request rejected.')
    leave.save()
    return redirect('admin_dashboard')

@login_required
def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

@login_required
def deleteAll(request):
    if not request.user.is_superuser: # Only a true superuser should do this
        messages.error(request, 'You are not authorized to perform this action.')
        return redirect('index')
    Account.objects.all().delete()
    messages.warning(request, "All accounts have been deleted.")
    return redirect('index')
