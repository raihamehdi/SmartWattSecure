# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Admin

def registeradmin(request):
    if request.method == 'POST':
        admin_name = request.POST.get('admin_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Create a new Admin instance and set the password
        admin = Admin(admin_name=admin_name, email=email)
        admin.password = make_password(password)
        admin.save()

        return redirect('registeradmin') 
    else:
        return render(request, 'registeradmin.html')

