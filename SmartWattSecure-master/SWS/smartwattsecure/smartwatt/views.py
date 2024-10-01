from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .arduino import get_mock_data, predict
from .models import EnergyData, CustomUser
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages

##-----SIGNUP VIEW-----##
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)
        return redirect('login') 
    return render(request, 'signup.html')   

##-----LOGIN VIEW-----##
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request, 'signup')
    return render(request, 'registration/login.html')

##-----DASHBOARD VIEW-----##
def dashboard(request):
    if request.method == 'GET':
        data = EnergyData.objects.all()
        return render(request, 'dashboard.html', {'data': data})

def dashboard(request):
    return render(request, 'dashboard.html')

def analytics(request):
    return render(request, 'analytics.html')

def contact(request):
    return render(request, 'contact.html')

def update_energy_data(request):
    if request.method == 'GET':
        data = get_mock_data()
        power = data['power']
        voltage = data['voltage']
        now = timezone.now()
        hour = now.hour  
        day_of_week = now.weekday()  
        month = now.month 
        X_test = [[power, voltage, hour, day_of_week, month]]
        predictions = predict(X_test)
        if predictions[0] == 0:  
            prediction_result = "normal"
        elif predictions[0] == 1:  
            prediction_result = "high"
        else:  
            prediction_result = "suspicious"

        EnergyData.objects.create(
            user = request.user,
            current=data['current'],
            power=data['power'],
            voltage=data['voltage'],
            total_units_consumed=data['total_units_consumed'],
            prediction=prediction_result,
            timestamp=now
        )
        
        return JsonResponse({'data': data, 'predictions': prediction_result})
    return JsonResponse({'status': 'failure'}, status=400)

def energy_data_api(request):
    data = EnergyData.objects.all()
    return JsonResponse(list(data.values()), safe=False)

def dashboard2(request):
    update_energy_data(request)
    return render(request, 'dashboard2.html')








