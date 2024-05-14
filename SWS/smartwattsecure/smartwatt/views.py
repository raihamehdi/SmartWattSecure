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

def registeradmin(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if Admin.objects.filter(email=email).exists():
            return render(request, 'registeradmin.html', {'error': 'Admin with this email already exists.'})
        else:
            admin = Admin(admin_name=admin_name, email=email)
            admin.password = make_password(password)
            admin.save()

            return redirect('admindash')
    else:
        return render(request, 'registeradmin.html')
    
    
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if Admin.objects.filter(Q(email=email) | Q(admin_name=username)).exists() or User.objects.filter(Q(email=email) | Q(username=username)).exists():
            return render(request, 'login_signup.html', {'error': 'Email or username already exists.'})
        else:
            user = User(username=username, email=email)
            user.password = make_password(password)
            user.save()

            return render(request, 'home.html') 
    else:
        return render(request, 'login_signup.html')


def login(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')

        user = User.objects.filter(email=email).first()
        if user is not None and check_password(password, user.password):
            return render(request, 'home.html')

        admin = Admin.objects.filter(email=email).first()
        if admin is not None and check_password(password, admin.password):
            return render(request, 'admindash.html')

        error_message = 'Invalid email or password.'
        return render(request, 'login_signup.html', {'error': error_message})

    else:
        return render(request, 'login_signup.html')

otp_storage = {}

def generate_otp():
    return str(random.randint(1000, 9999))  # Generate a 4-digit OTP

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Generate OTP
        otp = generate_otp()
        otp_storage[email] = otp  # Store the OTP temporarily (you might want to use a more secure storage)

        # Send OTP via email
        subject = 'Your OTP for Account Verification'
        html_message = render_to_string('emailtemp.html', {'otp': otp})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER  # Update with your email address or use a custom sender
        to_email = email
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

        return render(request, 'enterotp.html', {'email': email, 'otp': otp})
    else:
        return render(request, 'forgetpass.html')

# def verifyotp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         entered_otp = request.POST.get('otp')

#         if email in otp_storage and otp_storage[email] == entered_otp:
#             del otp_storage[email]  # Remove the OTP after successful verification

#             # Redirect to the password reset page or implement your logic here
#             return render(request, 'resetpass.html', {'email': email})
#         else:
#             return render(request, 'enterotp.html', {'email': email, 'error': 'Invalid OTP. Please try again.'})
#     else:
#         return redirect('forgetpass')
def home(request):
    return render(request, 'resetpass.html')