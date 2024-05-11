from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=30)
    password=models.CharField(max_length=20)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'{self.admin_id}, {self.admin_name}'
    


# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=10, default=" ")
#     password = models.CharField(max_length=50, default=" ")
#     location = models.TextField(default=" ")
#     admin = models.OneToOneField(Admin, on_delete=models.CASCADE, null=True)
#     owner = models.OneToOneField(LandOwner, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return f'{self.username}, {self.user_id}'