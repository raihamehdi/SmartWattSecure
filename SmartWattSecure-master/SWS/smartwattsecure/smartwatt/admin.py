from django.contrib import admin
from .models import CustomUser, EnergyData

admin.site.register(CustomUser)
admin.site.register(EnergyData)
