from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .arduino import data, predict
from .models import EnergyData, CustomUser
from datetime import datetime, time
from django.utils.timezone import localtime
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
    if request.user.is_authenticated:
        # Fetch the latest energy data for the logged-in user
        energy_data = EnergyData.objects.filter(user=request.user).order_by('-timestamp').first()

        return render(request, 'dashboard.html', {
            'energy_data': energy_data
        })
    else:
        return render(request, 'dashboard.html')

def help(request):
    return render(request, 'help.html')

def contact(request):
    return render(request, 'contact.html')

def update_energy_data(request):
    """Fetches new energy data from Arduino, saves it, and returns response."""
    arduino_data = data()
    if arduino_data:
        voltage, current, power, total_units_consumed, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440 = arduino_data
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()
        month = now.month

        # Prepare data for prediction
        X_test = [[power, voltage, hour, day_of_week, month, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440]]
        predictions = predict(X_test)
        if predictions[0] == 0:  
            prediction_result = "normal"
        elif predictions[0] == 1:  
            prediction_result = "high"
        else:  
            prediction_result = "suspicious"
        
        # Create a new EnergyData object for the user
        energy_data = EnergyData.objects.create(
            user=request.user,
            timestamp=now,
            voltage=voltage,
            current=current,
            power=power,
            total_units_consumed=total_units_consumed,
            prediction=prediction_result
        )

        energy_data.save()
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Failed to fetch data from Arduino'}, status=500)


def energy_data_api(request):
    if request.user.is_authenticated:
        update_response = update_energy_data(request)
        if update_response.status_code == 200:
            # Get the current time and start of the day (12 AM)
            now = datetime.now()
            start_of_day = datetime.combine(now.date(), time.min)  # Midnight

            # Filter energy data for the authenticated user since 12 AM
            user_data = EnergyData.objects.filter(
                user=request.user,
                timestamp__gte=start_of_day
            ).order_by('-timestamp')

            # Calculate total units consumed since 12 AM
            total_units_since_midnight = sum(item.total_units_consumed for item in user_data)

            # Prepare data for the latest record
            latest_data = user_data.first()
            local_timestamp = localtime(latest_data.timestamp)
            formatted_timestamp = local_timestamp.strftime('%I:%M %p')
            if latest_data:
                response_data = {
                    
                    'timestamp': formatted_timestamp, 
                    'voltage': latest_data.voltage,
                    'current': latest_data.current,
                    'power': latest_data.power,
                    'total_units_since_midnight': round(total_units_since_midnight, 2),
                    'total_units_consumed': latest_data.total_units_consumed,
                    'prediction': latest_data.prediction,
                }
            else:
                response_data = {
                    'total_units_since_midnight': 0,
                    'message': 'No data available since midnight.'
                }

            return JsonResponse(response_data, safe=False)
        return JsonResponse({'error': 'Failed to update data'}, status=500)
    return JsonResponse({'error': 'User not authenticated'}, status=403)



from .models import EnergyData
from datetime import timedelta

def units_consumed_view(request):
    filter_type = request.GET.get('filter', 'daily')  # Default to daily if no filter provided
    
    if filter_type == 'monthly':
        start_date = timezone.now() - timedelta(days=30)
    elif filter_type == 'weekly':
        start_date = timezone.now() - timedelta(days=7)
    else:  # Daily
        start_date = timezone.now() - timedelta(days=1)
    
    data = EnergyData.objects.all().values('timestamp', 'total_units_consumed')  # For testing all data
    
    response_data = [{"date": d["timestamp"].date(), "units": d["total_units_consumed"]} for d in data]
    return JsonResponse(response_data, safe=False)


