from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

class CustomUser(AbstractUser):
    pass

# class EnergyConsumption(models.Model):
#     consumption_id = models.AutoField(primary_key=True)
#     active_power = models.FloatField()
#     time = models.FloatField() 
#     user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False) 
#     @property
#     def consumption_data(self):
#         return self.active_power * self.time
#     def __str__(self):
#         return f'{self.consumption_id}, {self.active_power}, {self.consumption_data}, {self.user_id}'