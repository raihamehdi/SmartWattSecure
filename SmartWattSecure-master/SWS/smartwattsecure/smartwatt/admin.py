from django.contrib import admin
from .models import CustomUser, EnergyData, Anomaly

admin.site.register(CustomUser)
admin.site.register(EnergyData)
admin.site.register(Anomaly)

