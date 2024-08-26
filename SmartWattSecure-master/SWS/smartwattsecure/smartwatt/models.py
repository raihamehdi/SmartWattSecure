from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

class CustomUser(AbstractUser):
    pass

from django.db import models

class EnergyData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    total_units_consumed = models.FloatField()  # Add this field

    def __str__(self):
        return f"{self.timestamp} - Voltage: {self.voltage}V, Current: {self.current}A, Power: {self.power}W"
