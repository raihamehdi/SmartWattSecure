from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]
    CITY_CHOICES = [
        ('Sahiwal', 'Sahiwal'),
        ('Lahore', 'Lahore'),
        ('Islamabad', 'Islamabad'),
    ]
    REGION_CHOICES = {
        'Sahiwal': [
            ('Farid Town', 'Farid Town'),
            ('People’s Colony', 'People’s Colony'),
            ('Jogi Chowk', 'Jogi Chowk'),
        ],
        'Lahore': [
            ('Gulberg', 'Gulberg'),
            ('Johar Town', 'Johar Town'),
            ('DHA', 'DHA'),
        ],
        'Islamabad': [
            ('F-7', 'F-7'),
            ('G-10', 'G-10'),
            ('Blue Area', 'Blue Area'),
        ],
    }

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')  # Default role is 'User'
    city = models.CharField(max_length=15, choices=CITY_CHOICES, default='Sahiwal')  # Default city
    region = models.CharField(max_length=50, default='Farid Town')  # Default region

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required for other users

    def __str__(self):
        return f"{self.email} ({self.city}, {self.region})"

class EnergyData(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    total_units_consumed = models.FloatField()
    prediction = models.CharField(max_length=100)  

    def __str__(self):
        return f"UserID: {self.user.username}, Time recorded: {self.timestamp}, Prediction: {self.prediction} Voltage: {self.voltage}V, Current: {self.current}A, Power: {self.power}W, Total units Consumed:{self.total_units_consumed}"
    
class Anomaly(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()  # Number of consecutive suspicious predictions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anomaly for {self.user.username} from {self.start_time} to {self.end_time}"
    

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # To track if the notification is read
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:100]}"
