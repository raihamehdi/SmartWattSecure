# Create your views here.
import random
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Admin,User
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EnergyConsumption



def registeradmin(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if Admin.objects.filter(email=email).exists():
            # Admin already exists, redirect to error page
            return render(request, 'error.html', {'error_message': 'Admin with this email already exists!'})
        else:
            admin = Admin(admin_name=admin_name, email=email)
            admin.password = make_password(password)
            admin.save()

            return render(request, 'admindash.html')
    else:
        return render(request, 'registeradmin.html')

    
    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check for existing admin with same email or username
        existing_admin = Admin.objects.filter(Q(email=email) | Q(admin_name=username)).exists()

        # Check for existing user with same email or username
        existing_user = User.objects.filter(Q(email=email) | Q(username=username)).exists()

        if existing_admin:
            # Admin with duplicate email or username found
            error_message = "An admin with this email or username already exists!"
        elif existing_user:
            # User with duplicate email or username found
            error_message = "A user with this email or username already exists!"
        else:
            # No duplicates found, proceed with user creation
            user = User(username=username, email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'signin.html')

        # If duplicate found, render signup with error message
        return render(request, 'error.html', {'error_message': error_message})

    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'GET':  # Change to 'POST' for form submission
        email = request.GET.get('email')
        password = request.GET.get('password')

        user = User.objects.filter(email=email).first()
        admin = Admin.objects.filter(email=email).first()

        # Check for valid user credentials
        if user is not None and check_password(password, user.password):
            return render(request, 'home2.html')

        # Check for valid admin credentials
        elif admin is not None and check_password(password, admin.password):
            return render(request, 'admindash.html')

        # Handle incorrect credentials
        else:
            error_message = "Invalid email or password."
            return render(request, 'signin.html', {'error_message': error_message})

    else:
        return render(request, 'signin.html')


def sendotp(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print("email:", email)
        user = User.objects.filter(email=email).first()
        if user:
            reset_code = ''.join(random.choices('0123456789', k=4))
            send_mail(
                'Password Reset Code',
                f'Your password reset code is: {reset_code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            request.session['reset_code'] = reset_code
            request.session['reset_email'] = email
            return render(request, 'enterotp.html')
        else:
            error_message = "Email not found. Please enter a registered email address."
            return render(request, 'error.html', {'error_message': error_message})
    return render(request, 'forgetpass.html')


def verifyotp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('reset_code')
        email = request.session.get('reset_email')
        user_id = request.session.get('reset_user_id')  # Get user_id from session

        if entered_otp == saved_otp and user_id:
            
            request.session['reset_code'] = saved_otp
            request.session['reset_email'] = email
            return render(request, 'resetpass.html')
        else:
            error_message = "You have entered incorrect OTP."
            return render(request, 'error.html', {'error_message': error_message})

    return render(request, 'forgetpass.html')

def resetpass(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirmpassword = request.POST.get('confirmpassword')
        if(new_password == confirmpassword):
            email= request.session.get('reset_email')
            user = User.objects.filter(email=email).first()
            if user:
                user.password = make_password(new_password)
                user.save()
                del request.session['reset_code']
                del request.session['reset_email']
                return render(request, 'signin.html') 
        else:
            error_message = "passwords doesnt match"
            return render(request, 'error.html', {'error_message': error_message})      

    else:
        return render(request, 'resetpass.html')


def index(request):
    return render(request, 'index.html')

from django.shortcuts import render
from django.http import HttpResponse
from .models import EnergyConsumption

def home(request):
    # Get user_id from the request
    user_id = request.GET.get('user_id', None)

    # Check if user_id is provided and valid
    if user_id:
        try:
            # Get the user's consumption data
            latest_consumption = EnergyConsumption.objects.filter(user_id=user_id).order_by('-id').first()

            # Check if consumption data exists for the user
            if latest_consumption:
                active_power = latest_consumption.active_power
                consumption_data = latest_consumption.consumption_data
                username = latest_consumption.user_id.username
            else:
                active_power = 0  # Set default value if no data exists
                consumption_data = 0
                username = "Unknown"  # Set default username

            return render(request, 'home2.html', {
                'username': username,
                'active_power': active_power,
                'consumption_data': consumption_data,
            })
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    else:
        return HttpResponse("Please provide a valid user_id in the request.")




def energyc(request):
    if request.method == 'POST':
        active_power = request.POST.get('active_power')
        time = request.POST.get('time')
        user_id = request.POST.get('user_id')
        user = User.objects.get(user_id=user_id)
        consumption = EnergyConsumption.objects.create(
            active_power=active_power,
            time=time,
            user_id=user
        )
        consumption.save()
        
        return render(request,"consumptiondata.html" )
    
    else:
        consumptions = EnergyConsumption.objects.all()
        return render(request, 'consumptiondata.html', {'consumptions': consumptions})
    

