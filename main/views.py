#standerd
import json
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse

# third party
#local
from user.forms import PasswordChangeForm
from main.decorators import role_required
from main.functions import generate_form_errors, get_current_role

# Create your views here.
@login_required
def index(request):
    user_role =  get_current_role(request)
    
    if user_role == 'admin_user':
        return HttpResponseRedirect(reverse('main:admin_index'))
    elif user_role == 'staff':
        return HttpResponseRedirect(reverse('main:staff_index'))
    elif user_role == 'editor':
        return HttpResponseRedirect(reverse('main:editor_index'))
    elif user_role == 'student':
        return HttpResponseRedirect(reverse('main:student_index'))

@login_required
@role_required(['admin_user'])
def admin_index(request):
    
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Admin Dashboard',
        'dashboard_type' : "Admin Dashboard"  
    }
  
    return render(request,'pages/admin_user/admin_dashboard.html', context)

@login_required
@role_required(['editor'])
def editor_index(request):
    
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Editor Dashboard',
        'dashboard_type' : "Editor Dashboard" 
    }
  
    return render(request,'pages/editor/editor_dashboard.html', context)

@login_required
@role_required(['staff'])
def staff_index(request):
    
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Staff Dashboard',
        'dashboard_type' : "Staff Dashboard" 
    }
  
    return render(request,'pages/staff/staff_dashboard.html', context)

@login_required
@role_required(['student'])
def student_index(request):
    
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Student Dashboard',
        'dashboard_type' : "Student Dashboard" 
    }
  
    return render(request,'pages/students/student_dashboard.html', context)

