from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .arduino import data, predict
from .models import EnergyData, CustomUser, Anomaly, Notification
from datetime import datetime, time, timedelta
from django.utils.timezone import localtime, localdate
from django.utils import timezone
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
<<<<<<< HEAD
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter


=======
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib.auth import logout
>>>>>>> f61534a6dfe5d08f9429f0bc9964a6bf4efbb09d

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

# User Settings
def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Update password only if provided
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])

            user.save()
            messages.success(request, "Your profile was updated successfully!")
        else:
            messages.error(request, "Form submission failed: {}".format(form.errors))

        # Redirect to the same page
        return redirect(request.META.get('HTTP_REFERER', '/'))

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

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

def analytics(request):
    return render(request, 'analytics.html')

def help(request):
    return render(request, 'help.html')

def contact(request):
    return render(request, 'contact.html')

##-----UPDATE ENERGYDATA VIEW-----##

def update_energy_data(request):
    """Fetches new energy data from Arduino, saves it, and returns response."""
    arduino_data = data()
    if arduino_data:
        voltage, current, power, total_units_consumed, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440 = arduino_data
        now = timezone.now()
        
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


##-----ENERGYDATA VIEW-----##
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

##-----WEEKLY VIEW-----##
def weekly_data(request):
    if request.user.is_authenticated:
        # Define the date range (last 7 days)
        today = timezone.localdate()  # Get the current date only
        start_date = today - timedelta(days=6)

        # Get the current datetime, including hours, minutes, and seconds
        now = timezone.now()

        # Query the database for the last 7 days, but include today's data up to the current time
        energy_data = EnergyData.objects.filter(
            user=request.user,
            timestamp__gte=start_date,  # Query the raw timestamp without timezone conversion
            timestamp__lte=now          # Use the current timestamp instead of just today
        ).extra(
            select={'timestamp_date': 'DATE(timestamp)'}  # Group by date only
        ).values('timestamp_date').annotate(total_units=Sum('total_units_consumed')).order_by('timestamp_date')

        # Prepare daily totals, ensuring all 7 days are covered
        time_labels = [(start_date + timedelta(days=i)) for i in range(7)]
        daily_totals = {entry['timestamp_date']: entry['total_units'] for entry in energy_data}
        units_consumed = [round(daily_totals.get(day, 0), 2) for day in time_labels]

        # Prepare response data
        response_data = {
            "labels": time_labels,  # Chart.js expects this
            "units consumed": units_consumed
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

##-----MONTHLY VIEW-----##
def monthly_data(request):
    if request.user.is_authenticated:
        # Define the date range (last 30 days)
        today = timezone.localdate()
        start_date = today - timedelta(days=29)
        now=timezone.now()

        # Query the database for the last 30 days
        energy_data = EnergyData.objects.filter(
            user=request.user,
            timestamp__gte=start_date,
            timestamp__lte=now
        ).extra(
            select={'timestamp_date': 'DATE(timestamp)'}
        ).values('timestamp_date').annotate(total_units=Sum('total_units_consumed')).order_by('timestamp_date')

        # Prepare daily totals, ensuring all 30 days are covered
        time_labels = [(start_date + timedelta(days=i)) for i in range(30)]
        daily_totals = {entry['timestamp_date']: entry['total_units'] for entry in energy_data}
        units_consumed = [round(daily_totals.get(day, 0), 2) for day in time_labels]

        # Prepare response data
        response_data = {
            "labels": time_labels,  # Chart.js expects this
            "units consumed": units_consumed
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)



##-----ANOMALIES VIEW-----##
@receiver(post_save, sender=EnergyData)
def check_anomaly_every_ten_entries(sender, instance, **kwargs):
    user = instance.user  # Get the user associated with this energy data

    # Count total entries for the user
    total_entries = EnergyData.objects.filter(user=user).count()

    # Check only after every 10 entries
    if total_entries % 10 == 0:  # Trigger anomaly check
        check_and_log_anomaly(user)

def check_and_log_anomaly(user):
    # Retrieve the last 10 predictions marked as "suspicious"
    recent_predictions = list(
        EnergyData.objects.filter(
            user=user,
            prediction="suspicious"
        ).order_by('-timestamp')[:10]
    )

    # Check if there are exactly 10 predictions
    if len(recent_predictions) < 10:
        return  # Exit if not enough data

    # Extract start and end timestamps for the anomaly
    start_time = recent_predictions[-1].timestamp  # Earliest of the 10
    end_time = recent_predictions[0].timestamp  # Latest of the 10

    # Log the anomaly
    Anomaly.objects.create(
        user=user,
        start_time=start_time,
        end_time=end_time,
        count=len(recent_predictions)
    )
    

##-----ANOMALY CHART VIEW-----##
def get_anomalies(request):
    if request.user.is_authenticated:
        # Define the date range (last 7 days)
        today = timezone.localdate()  # Get the current date only
        start_date = today - timedelta(days=6)
        now = timezone.now()
        
        # Fetch anomalies that occurred in the last 7 days
        anomalies = Anomaly.objects.filter(
            user=request.user,
            start_time__gte=start_date,
            end_time__lte=now
        ).values('start_time', 'end_time')

        # Count anomalies per day
        anomaly_counts = Counter()  # Dictionary to store anomaly counts per day
        for anomaly in anomalies:
            anomaly_date = anomaly['start_time'].date()
            anomaly_counts[anomaly_date] += 1

        # Prepare the count for each of the last 7 days
        time_labels = [start_date + timedelta(days=i) for i in range(7)]
        anomaly_data = [anomaly_counts.get(day, 0) for day in time_labels]  # Default to 0 if no anomalies

        # Prepare response data
        response_data = {
            "labels": [str(day) for day in time_labels],  # Date labels for the last 7 days
            "anomalies": anomaly_data  # Total count of anomalies per day
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

##-----NOTIFICATIONS VIEW-----##
def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        response_data = [
            {
                "date": notification.timestamp.strftime("%m/%d/%Y"),
                "message": notification.message,
            }
            for notification in notifications
        ]
        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

@receiver(post_save, sender=Anomaly)
def create_notification_for_anomaly(sender, instance, created, **kwargs):
    if created:
        message = f"Power anomaly detected from {instance.start_time.strftime('%H:%M')} to {instance.end_time.strftime('%H:%M')}."
        Notification.objects.create(user=instance.user, message=message)










