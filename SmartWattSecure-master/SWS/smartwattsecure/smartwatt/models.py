from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

from django.db import models

class EnergyData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    reactive_power = models.FloatField()
    total_units_consumed = models.FloatField()
    prediction = models.CharField(max_length=100)  

    def __str__(self):
        return f"Time recorded: {self.timestamp}, Prediction: {self.prediction} Voltage: {self.voltage}V, Current: {self.current}A, Power: {self.power}W, Reactive Power: {self.reactive_power}W, Total units Consumed:{self.total_units_consumed}"
