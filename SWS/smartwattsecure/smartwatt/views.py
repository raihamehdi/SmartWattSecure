# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Admin,User
from django.db.models import Q

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