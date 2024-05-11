# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Admin,User

def registeradmin(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if an admin with the provided email already exists
        if Admin.objects.filter(email=email).exists():
            return render(request, 'registeradmin.html', {'error': 'Admin with this email already exists.'})
        else:
            # Create a new Admin instance and set the password
            admin = Admin(admin_name=admin_name, email=email)
            admin.password = make_password(password)
            admin.save()

            return redirect('admindash')
    else:
        return render(request, 'registeradmin.html')
    


def login(request):
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     try:
    #         # Check if the login credentials belong to a user
    #         user = User.objects.get(email=email)
    #         if check_password(password, user.password):
    #             # Authentication successful for user, redirect to home page
    #             return redirect('home')  # Adjust 'home' to your home page URL name
    #     except User.DoesNotExist:
    #         pass  # User with the provided email doesn't exist, continue checking for admin

    #     try:
    #         # Check if the login credentials belong to an admin
    #         admin = Admin.objects.get(email=email)
    #         if check_password(password, admin.password):
    #             # Authentication successful for admin, redirect to admin dashboard
    #             return redirect('admindash')  # Adjust 'admindash' to your admin dashboard URL name
    #     except Admin.DoesNotExist:
    #         pass  # Admin with the provided email doesn't exist

    #     # If no user or admin with the provided credentials is found, show login page again with error
    #     error_message = 'Invalid email or password.'
    #     return render(request, 'login_signup.html', {'error': error_message})
    # else:
        return render(request, 'login_signup.html')

