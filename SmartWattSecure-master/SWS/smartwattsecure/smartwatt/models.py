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
    ('Karachi', 'Karachi'),
    ('Rawalpindi', 'Rawalpindi'),
    ('Faisalabad', 'Faisalabad'),
    ('Multan', 'Multan'),
    ('Peshawar', 'Peshawar'),
    ('Quetta', 'Quetta'),
    ('Gujranwala', 'Gujranwala'),
    ('Sialkot', 'Sialkot'),
    ('Mardan', 'Mardan'),
    ('Bahawalpur', 'Bahawalpur'),
    ('Murree', 'Murree'),
    ('Abbottabad', 'Abbottabad'),
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
        'Karachi': [
            ('Korangi', 'Korangi'),
            ('Clifton', 'Clifton'),
            ('Saddar', 'Saddar'),
        ],
        'Rawalpindi': [
            ('Murree Road', 'Murree Road'),
            ('Satellite Town', 'Satellite Town'),
            ('Committee Chowk', 'Committee Chowk'),
        ],
        'Faisalabad': [
            ('Satyana Road', 'Satyana Road'),
            ('Jaranwala Road', 'Jaranwala Road'),
            ('Kohinoor City', 'Kohinoor City'),
        ],
        'Multan': [
            ('Cantt', 'Cantt'),
            ('Bosan Road', 'Bosan Road'),
            ('City Centre', 'City Centre'),
        ],
        'Peshawar': [
            ('University Road', 'University Road'),
            ('Hayatabad', 'Hayatabad'),
            ('Fazal Town', 'Fazal Town'),
        ],
        'Quetta': [
            ('Jinnah Road', 'Jinnah Road'),
            ('Kohlu', 'Kohlu'),
            ('Saryab', 'Saryab'),
        ],
        'Gujranwala': [
            ('Wazirabad Road', 'Wazirabad Road'),
            ('Model Town', 'Model Town'),
            ('Gulshan-e-Iqbal', 'Gulshan-e-Iqbal'),
        ],
        'Sialkot': [
            ('Daska Road', 'Daska Road'),
            ('Saddar', 'Saddar'),
            ('Sambrial', 'Sambrial'),
        ],
        'Mardan': [
            ('Main Bazaar', 'Main Bazaar'),
            ('Shahbaz Garh', 'Shahbaz Garh'),
            ('Mardan Cantt', 'Mardan Cantt'),
        ],
        'Bahawalpur': [
            ('Darbar Road', 'Darbar Road'),
            ('Layyah Road', 'Layyah Road'),
            ('Bahawal Stadium', 'Bahawal Stadium'),
        ],
        'Murree': [
            ('Mall Road', 'Mall Road'),
            ('Kashmir Point', 'Kashmir Point'),
            ('Lower Topa', 'Lower Topa'),
        ],
        'Abbottabad': [
            ('Mansehra Road', 'Mansehra Road'),
            ('Havelian', 'Havelian'),
            ('Abbottabad City', 'Abbottabad City'),
        ],
    }


    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')  # Default role is 'User'
    city = models.CharField(max_length=15, choices=CITY_CHOICES, default='Sahiwal')  # Default city
    region = models.CharField(max_length=50, default='Farid Town')  # Default region
    is_restricted = models.BooleanField(default=False) 

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


class ContactMessage(models.Model):
    USER_TYPE_CHOICES = [
        ('visitor', 'Visitor'),
        ('user', 'User'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='visitor')
    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.user_type}"
    

