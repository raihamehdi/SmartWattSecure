from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .arduino import data, predict
from .models import EnergyData, CustomUser, Anomaly, Notification, ContactMessage
from datetime import datetime, time, timedelta
from django.utils.timezone import localtime, localdate, now, make_aware
from django.utils import timezone
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import random
from django.conf import settings
from django.utils.timezone import make_aware, now 
from pytz import timezone as pytz_timezone 
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
import json

##-----SIGNUP VIEW-----##
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')  # Get city from the form
        region = request.POST.get('region')  # Get region from the form

        # Create the user with the additional city and region fields
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            city=city,
            region=region
        )
        
        # Automatically log in the user after signup
        auth_login(request, user)
        return redirect('login') 

    return render(request, 'signup.html')


@login_required
def adminview(request):
    if not request.user.is_staff:
        return redirect('index')

    today = datetime.today().date()

    first_day_of_current_month = today.replace(day=1)

    first_day_of_current_month = datetime.combine(first_day_of_current_month, datetime.min.time())
    today_datetime = datetime.combine(today, datetime.min.time()) 
    first_day_of_current_month = make_aware(first_day_of_current_month)
    today_datetime = make_aware(today_datetime)

    cities = CustomUser.objects.values_list('city', flat=True).distinct()
    city_regions = {}
    users = CustomUser.objects.filter(is_staff=False)
    user_data = []

    for user in users:
        energy_data = EnergyData.objects.filter(
            user=user,
            timestamp__gte=first_day_of_current_month,
            timestamp__lte=today_datetime
        )
        total_units = energy_data.aggregate(total_units=Sum('total_units_consumed'))['total_units'] or 0
        user_data.append({
            'user': user,
            'total_units': round(total_units, 2),
        })

    for city in cities:
        city_regions[city] = CustomUser.REGION_CHOICES.get(city, [])

    messages = ContactMessage.objects.all()
    return render(request, 'admin.html', {'cities': cities, 'city_regions': city_regions, "user_data": user_data, "messages": messages})


##-----LOGIN VIEW-----##
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_restricted: 
                return JsonResponse({'success': False, 'error_message': 'Your account is restricted. Please contact support.'})
            auth_login(request, user)
            if user.role == 'User':
                return JsonResponse({'success': True, 'redirect_url': '/dashboard'})
            elif user.role == 'Admin':
                return JsonResponse({'success': True, 'redirect_url': '/adminview'})
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid email or password'})
    return render(request, 'registration/login.html')

# User Updation
@login_required
def edit_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            return redirect('dashboard')  # Redirect to the dashboard after saving
    return render(request, 'edit_username.html')

@login_required
def edit_email(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if new_email:
            request.user.email = new_email
            request.user.save()
            return redirect('dashboard')
    return render(request, 'edit_email.html')

@login_required
def edit_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        if new_password:
            request.user.set_password(new_password)
            request.user.save()
            return redirect('dashboard')
    return render(request, 'edit_password.html')

# View for Forget Password Page
def forgot_password_view(request):
    return render(request, 'forgetpass.html')  # Render the forget password page template

def verifyotp(request):
    return render(request, 'enterotp.html')

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


def energy_data_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)
    
    # Fetch new energy data from Arduino
    arduino_data = data()
    if arduino_data:
        voltage, current, power, total_units_consumed, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440 = arduino_data
        now_utc = now()
        now_local = localtime(now_utc)
        hour = now_local.hour
        day_of_week = now_local.weekday()
        month = now_local.month

        # Prepare data for prediction
        X_test = [[power, voltage, hour, day_of_week, month, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440]]
        predictions = predict(X_test)
        prediction_result = (
            "normal" if predictions[0] == 0 
            else "high" if predictions[0] == 1 
            else "suspicious"
        )
        nowz = pytz_timezone("Asia/Karachi")
        todayTime= datetime.now(nowz).timestamp()
        # Save the data to the database
        EnergyData.objects.create(
            user=request.user,
            timestamp=todayTime,
            voltage=voltage,
            current=current,
            power=power,
            total_units_consumed=total_units_consumed,
            prediction=prediction_result
        )
    else:
        return JsonResponse({'error': 'Failed to fetch data from Arduino'}, status=500)

    # Retrieve data since midnight
    start_of_day_local = datetime.combine(now_local.date(), time.min)  # Midnight in local timezone
    start_of_day_utc = make_aware(start_of_day_local).astimezone(pytz_timezone('UTC'))  # Convert to UTC
    user_data = EnergyData.objects.filter(
        user=request.user,
        timestamp__gte=start_of_day_utc
    ).order_by('-timestamp')

    # Calculate total units consumed since 12 AM
    total_units_since_midnight = sum(item.total_units_consumed for item in user_data)

    # Prepare the latest data for the response
    latest_data = user_data.first()
    if latest_data:
        # local_timestamp = localtime(latest_data.timestamp)
        formatted_timestamp = datetime.now(nowz)
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


##-----WEEKLY VIEW-----##
def weekly_data(request):
    if request.user.is_authenticated:
        today = timezone.localdate()  
        start_date = today - timedelta(days=6)
        now = timezone.now()
        energy_data = EnergyData.objects.filter(
            user=request.user,
            timestamp__gte=start_date,  
            timestamp__lte=now          
        ).extra(
            select={'timestamp_date': 'DATE(timestamp)'}  
        ).values('timestamp_date').annotate(total_units=Sum('total_units_consumed')).order_by('timestamp_date')
        time_labels = [(start_date + timedelta(days=i)) for i in range(7)]
        daily_totals = {entry['timestamp_date']: entry['total_units'] for entry in energy_data}
        units_consumed = [round(daily_totals.get(day, 0), 2) for day in time_labels]
        response_data = {
            "labels": time_labels,  
            "units consumed": units_consumed
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

##-----MONTHLY VIEW-----##
def monthly_data(request):
    if request.user.is_authenticated:
        # Define the date range from the 1st of the current month to today
        today = timezone.localdate()
        start_date = today.replace(day=1)
        now = timezone.now()

        # Query the database from the start of the month to today
        energy_data = EnergyData.objects.filter(
            user=request.user,
            timestamp__gte=start_date,
            timestamp__lte=now
        ).extra(
            select={'timestamp_date': 'DATE(timestamp)'}
        ).values('timestamp_date').annotate(total_units=Sum('total_units_consumed')).order_by('timestamp_date')

        # Prepare daily totals, ensuring all days from the start of the month to today are covered
        num_days = (today - start_date).days + 1  # Number of days from start_date to today
        time_labels = [(start_date + timedelta(days=i)) for i in range(num_days)]
        daily_totals = {entry['timestamp_date']: entry['total_units'] for entry in energy_data}
        units_consumed = [round(daily_totals.get(day, 0), 2) for day in time_labels]

        # Prepare response data
        response_data = {
            "labels": [day.strftime('%b %d') for day in time_labels],  # Format dates for Chart.js
            "units consumed": units_consumed
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

##-----YEARLY VIEW-----##
def yearly_data(request):
    if request.user.is_authenticated:
        # Define the date range (last 12 months)
        today = timezone.localdate()
        start_date = today.replace(month=1, day=1)  # Start from the first day of the year
        now = timezone.now()

        # Query the database for the whole year (12 months)
        energy_data = EnergyData.objects.filter(
            user=request.user,
            timestamp__gte=start_date,
            timestamp__lte=now
        ).extra(
            select={'timestamp_month': 'EXTRACT(MONTH FROM timestamp)'}  # Extract month from timestamp
        ).values('timestamp_month').annotate(total_units=Sum('total_units_consumed')).order_by('timestamp_month')

        # Prepare monthly totals, ensuring all 12 months are covered
        time_labels = [start_date.replace(month=i) for i in range(1, 13)]  # List of months
        monthly_totals = {entry['timestamp_month']: entry['total_units'] for entry in energy_data}
        units_consumed = [round(monthly_totals.get(i, 0), 2) for i in range(1, 13)]  # Default 0 for missing months

        # Prepare response data
        response_data = {
            "labels": [month.strftime('%b') for month in time_labels],  # Month names (e.g., Jan, Feb)
            "units consumed": units_consumed
        }

        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

##-----ANOMALIES VIEW-----##
@login_required
def check_and_create_anomaly(request):
    user = request.user  # Get the current authenticated user

    # Retrieve the last 15 predictions marked as "suspicious"
    recent_predictions = list(
        EnergyData.objects.filter(
            user=user,
            prediction__icontains="suspicious"  # Adjust filter for partial matches
        ).order_by('-timestamp')[:15]
    )
    print("Filtered Predictions:", recent_predictions)

    # Check if there are enough valid "suspicious" predictions
    if len(recent_predictions) < 15 or not all(
        pred.prediction.lower().startswith("suspicious") for pred in recent_predictions
    ):
        return JsonResponse({"message": "Not enough valid suspicious predictions."}, status=400)

    # Extract the start and end timestamps for the anomaly
    start_time = recent_predictions[-1].timestamp  # Earliest of the 15
    end_time = recent_predictions[0].timestamp  # Latest of the 15

    # Check if an anomaly with the same time range already exists
    existing_anomaly = Anomaly.objects.filter(
        user=user,
        start_time__lte=end_time,
        end_time__gte=start_time
    ).exists()

    if existing_anomaly:
        return JsonResponse({"message": "Anomaly already exists for this time range."}, status=400)

    # Create an anomaly entry
    anomaly = Anomaly.objects.create(
        user=user,
        start_time=start_time,
        end_time=end_time,
        count=len(recent_predictions)
    )

    # Send email notification to the user
    subject = "Suspicious Energy Consumption Detected"
    message = (
        f"Dear {user.username},\n\n"
        f"An anomaly in your energy consumption was detected.\n"
        f"Details:\n"
        f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Data entries are showing suspicious behaviour. Please review your energy consumption."
    )
    recipient_list = [user.email]

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

    return JsonResponse({"message": "Anomaly created successfully.", "start_time": start_time, "end_time": end_time, "count": len(recent_predictions)})



@login_required
def get_today_anomalies(request):
    user = request.user

    karachi_tz = pytz_timezone("Asia/Karachi")

    today_start = make_aware(datetime.combine(now().astimezone(karachi_tz), datetime.min.time()), karachi_tz)
    today_end = make_aware(datetime.combine(now().astimezone(karachi_tz), datetime.max.time()), karachi_tz)

    anomalies_count = Anomaly.objects.filter(
        user=user,
        start_time__range=(today_start, today_end)
    ).count()

    return JsonResponse({"today_anomalies": anomalies_count})


def get_anomalies_data(request, timeframe):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    nowz = pytz_timezone("Asia/Karachi")
    todayTime= datetime.now(nowz).timestamp()

    if timeframe == 'weekly':
        start_date = todayTime - timedelta(days=6)
        time_labels = [start_date + timedelta(days=i) for i in range(7)] 
        label_format = "%Y-%m-%d"  
        start_date = todayTime.replace(day=1)
        days_in_month = (todayTime - start_date).days + 1
        time_labels = [start_date + timedelta(days=i) for i in range(days_in_month)]
        label_format = "%d"
    elif timeframe == 'yearly':
        start_date = todayTime.replace(month=1, day=1)  
        time_labels = [start_date.replace(month=i) for i in range(1, 13)] 
        label_format = "%b"  
    else:
        return JsonResponse({'error': 'Invalid timeframe'}, status=400)

    # Fetch anomalies within the timeframe
    anomalies = Anomaly.objects.filter(
        user=request.user,
        start_time__gte=start_date,
        end_time__lte=now
    ).values('start_time')

    # Count anomalies based on timeframe granularity
    anomaly_counts = Counter()
    for anomaly in anomalies:
        if timeframe == 'yearly':
            anomaly_date = anomaly['start_time'].date().replace(day=1)  # Group by month
        else:
            anomaly_date = anomaly['start_time'].date()  # Group by day
        anomaly_counts[anomaly_date] += 1

    # Prepare anomaly counts for each label
    anomaly_data = [anomaly_counts.get(label, 0) for label in time_labels]

    # Prepare response data
    response_data = {
        "labels": [label.strftime(label_format) for label in time_labels],
        "anomalies": anomaly_data
    }
    return JsonResponse(response_data, safe=False)

# Individual Views
def get_weekly_anomalies(request):
    return get_anomalies_data(request, timeframe='weekly')

def get_monthly_anomalies(request):
    return get_anomalies_data(request, timeframe='monthly')

def get_yearly_anomalies(request):
    return get_anomalies_data(request, timeframe='yearly')



##-----NOTIFICATIONS VIEW-----##

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        
        response_data = [
            {
                "id": notification.id,  # Add the ID for each notification
                "date": notification.timestamp.strftime("%m/%d/%Y"),
                "message": notification.message,
                "is_read": notification.is_read  # Include the is_read field
            }
            for notification in notifications
        ]
        
        return JsonResponse(response_data, safe=False)

    return JsonResponse({'error': 'User not authenticated'}, status=403)

# Signal to create a notification when an anomaly is detected
@receiver(post_save, sender=Anomaly)
def create_notification_for_anomaly(sender, instance, created, **kwargs):
    if created:
        message = f"Power anomaly detected at {instance.start_time.strftime('%H:%M')}."
        Notification.objects.create(user=instance.user, message=message)

def sendotp(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print("email:", email)
        user = CustomUser.objects.filter(email=email).first()
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

        if entered_otp == saved_otp:
            
            request.session['reset_code'] = saved_otp
            request.session['reset_email'] = email
            return render(request, 'resetpass.html')


    return render(request, 'forgetpass.html')

def resetpass(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirmpassword = request.POST.get('confirmpassword')
        if(new_password == confirmpassword):
            email= request.session.get('reset_email')
            user = CustomUser.objects.filter(email=email).first()
            if user:
                user.password = make_password(new_password)
                user.save()
                del request.session['reset_code']
                del request.session['reset_email']
                return redirect('login')
        else:
            error_message = "passwords doesnt match"
            return render(request, 'error.html', {'error_message': error_message})      

    else:
        return render(request, 'resetpass.html')

def inquiry_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        user_type = 'user' if request.user.is_authenticated else 'visitor'
        ContactMessage.objects.create(name=name, email=email, message=message, user_type=user_type)
        return JsonResponse({'message': 'Message sent successfully!'})    
    return HttpResponse(status=405) 


def city_regions_view(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            # Get the regions for the selected city
            regions = CustomUser.REGION_CHOICES.get(city, [])
            data = []

            tz = pytz_timezone.timezone('Asia/Karachi')
            now = datetime.now(tz)

            # Get the start and end of the current month
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_of_month = (start_of_month.replace(month=start_of_month.month % 12 + 1) - timedelta(days=1))

            # Get the total units consumed for each region for the current month
            for region_code, region_name in regions:
                total_units = EnergyData.objects.filter(
                    user__region=region_code,
                    timestamp__gte=start_of_month,
                    timestamp__lte=end_of_month
                ).aggregate(total_units=Sum("total_units_consumed"))
                data.append({
                    "region": region_name,
                    "total_units": total_units["total_units"] or 0,
                })


            return JsonResponse({"regions": data})

        return JsonResponse({"error": "City not provided."}, status=400)

    # If it's a GET request, you can either handle it as a default case or just return a simple response.
    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

def delete_user_ajax(request, user_id):
    if request.method == "POST":  # Ensure it's an AJAX POST request
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Failed to delete user'})

def admin_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff:
                auth_login(request, user)
                return JsonResponse({"status": "success", "redirect_url": "/adminpanel/"})
            return JsonResponse({"status": "error", "message": "Invalid email or password!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return render(request, "admin-login.html")

@csrf_exempt
def toggle_user_restriction(request, user_id):
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            user.is_restricted = not user.is_restricted  # Toggle restriction status
            user.save()
            status = "restricted" if user.is_restricted else "unrestricted"
            return JsonResponse({
                "success": True,
                "message": f"User {user.username} {status} successfully.",
                "new_status": status
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"})
    return JsonResponse({"success": False, "message": "Invalid request method."})
    

@csrf_exempt
def restrict_user(request, user_id):
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            print(user)
            user.is_restricted = True 
            user.save()
            return JsonResponse({"success": True, "message": f"User {user.username} restricted successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"})
    return JsonResponse({"success": False, "message": "Invalid request method."})

def resend_otp(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')  # Get email from session
        
        if not email:
            return JsonResponse({"success": False, "error": "No email found in session."})
        
        # Generate a new OTP
        otp = str(random.randint(1000, 9999))  # Generate a new 4-digit OTP
        
        # Send the OTP to the email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        
        # Store new OTP in session
        request.session['reset_code'] = otp
        
        # Respond with success, no need for messages
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request method."})


def inquiry_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        user_type = 'user' if request.user.is_authenticated else 'visitor'
        ContactMessage.objects.create(name=name, email=email, message=message, user_type=user_type)
        return JsonResponse({'message': 'Message sent successfully!'})    
    return HttpResponse(status=405) 


def city_regions_view(request):
    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            # Get the regions for the selected city
            regions = CustomUser.REGION_CHOICES.get(city, [])
            data = []

            # Get the total units consumed for each region
            for region_code, region_name in regions:
                total_units = EnergyData.objects.filter(user__region=region_code).aggregate(total_units=models.Sum("total_units_consumed"))
                data.append({
                    "region": region_name,
                    "total_units": total_units["total_units"] or 0,
                })

            return JsonResponse({"regions": data})

        return JsonResponse({"error": "City not provided."}, status=400)

    # If it's a GET request, you can either handle it as a default case or just return a simple response.
    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

def delete_user_ajax(request, user_id):
    if request.method == "POST":  # Ensure it's an AJAX POST request
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'User deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Failed to delete user'})

def admin_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff:
                auth_login(request, user)
                return JsonResponse({"status": "success", "redirect_url": "/adminpanel/"})
            return JsonResponse({"status": "error", "message": "Invalid email or password!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return render(request, "admin-login.html")

def logout_admin(request):
    if request.method == "POST":
        logout(request)
        return render(request, "admin-login.html")  # Use URL name for better flexibility
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@csrf_exempt
def restrict_user(request, user_id):
    if request.method == "POST":
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            print(user)
            user.is_restricted = True 
            user.save()
            return JsonResponse({"success": True, "message": f"User {user.username} restricted successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"})
    return JsonResponse({"success": False, "message": "Invalid request method."})


@csrf_exempt
def mark_notification_read(request, notification_id):
    if request.method == "POST":
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse({"error": "Notification not found"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)

def unread_notification_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({"unread_count": unread_count})
    return JsonResponse({"error": "User not authenticated"}, status=403)