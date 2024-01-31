#standerd
import json
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http.response import HttpResponseRedirect, HttpResponse

# third party
#local
from user.forms import *
from main.decorators import role_required
from main.functions import encrypt_message, generate_form_errors, get_auto_id, get_current_role
from user.models import UserDetails

# Create your views here.
def sign_up(request):
    response_data = {}
    if request.method == 'POST':
        form = userDetailsForm(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    email = form.cleaned_data['email']   
                
                    user_data = User.objects.create_user(
                            username=email,
                            password=form.cleaned_data['password'], 
                        )
                    
                    if Group.objects.filter(name=form.cleaned_data['role']).exists():
                        group = Group.objects.get(name=form.cleaned_data['role'])
                    else:
                        group = Group.objects.create(name=form.cleaned_data['role'])

                    user_data.groups.add(group)
                    
                    data = form.save(commit=False)
                    data.auto_id = get_auto_id(UserDetails)
                    data.creator = user_data
                    data.date_updated = datetime.datetime.today()
                    data.updater = user_data
                    data.user = user_data
                    data.password = encrypt_message(form.cleaned_data['password'])
                    data.save()
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "User created successfully.",
                        "redirect": "true",
                        "redirect_url": reverse('user:login'),
                    }
                    
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Integrity error occurred. Please check your data.",
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(form, formset=False)

            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
    
    else :
        signup_form = userDetailsForm()
        
        context = {
        "signup_form" :signup_form,
        "page_name" : 'Registration',
        "url": reverse('user:signup'),
    }
    return render(request,'registration/registration.html',context)


def signin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    
                    return HttpResponseRedirect(reverse('main:index'))
                else:
                    response_data = {
                        "status": "false",
                        "title": "Not Match",
                        "message": "username and password do not match",
                    }
            else:
                response_data = {
                    "status": "false",
                    "title": "Error",
                    "message": "Incorrect username",
                }
        else:
            message = generate_form_errors(form, formset=False)
            response_data = {
                "status": "false",
                "title": "Error",
                "message": message,
            }
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else :
        form = UserLoginForm()
        
        context = {
            'form': form,
        }
    
        return render(request,'registration/login.html',context)


# @login_required
# def change_password(request):
    
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.POST)
#         password_matches = check_password(request.POST.get("current_password"), request.user.password)
        
#         if password_matches:
#             print("matched")
#             if form.is_valid():
#                 print("valid")
                
#                 usr = User.objects.get(pk=request.user.pk)
#                 usr.set_password(form.cleaned_data['password'])
#                 usr.save()
                
#                 response_data = {
#                     "status": "true",
#                     "title": "Successful",
#                     "message": "Password Updated Successfully",
#                     'redirect': 'true',
#                     'redirect_url': reverse("main:profile")
#                 }
#             else:
#                 print("not valid")
#                 message = generate_form_errors(form, formset=False)
#                 response_data = {
#                     "status": "false",
#                     "title": "Filed",
#                     "message": message,
#                 }
#         else:
#             print("not match")
#             response_data = {
#                 "status": "false",
#                 "title": "Filed",
#                 "message": "current password not match",
#             }
            
#     return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
# @login_required
# def profile(request):
    
#     instance = User.objects.get(pk=request.user.pk)
#     form = PasswordChangeForm()
    
#     context = {
#         'instance': instance,
#         'form': form,
#     }

#     return render(request,'admin_panel/pages/profile.html', context)