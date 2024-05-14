from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return f'{self.admin_id}, {self.admin_name}'
    
    
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def __str__(self):
        return f'{self.user_id}, {self.username}'

class EnergyConsumption(models.Model):
    consumption_id = models.AutoField(primary_key=True)
    active_power = models.FloatField()
    time = models.FloatField() 
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=False) 
    @property
    def consumption_data(self):
        return self.active_power * self.time
    def __str__(self):
        return f'{self.consumption_id}, {self.active_power}, {self.consumption_data}, {self.username}'
    
#    def average_active_power(self):
#         time_range = EnergyConsumption.objects.filter(timestamp__lte=self.timestamp).aggregate(avg_active_power=Avg('active_power'))
#         return time_range['avg_active_power'] or 0  
#     def consumption_data(self):
#         avg_power = self.average_active_power()
#         return avg_power * self.time 
