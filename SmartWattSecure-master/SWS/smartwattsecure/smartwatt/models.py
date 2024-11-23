from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Ensure you set USERNAME_FIELD to 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    count = models.IntegerField()  # Number of consecutive suspicious predictions
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anomaly for {self.user.username} from {self.start_time} to {self.end_time}"

