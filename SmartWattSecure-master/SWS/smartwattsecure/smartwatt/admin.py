from django.contrib import admin
from .models import CustomUser, EnergyData, Anomaly, Notification

admin.site.register(CustomUser)
admin.site.register(EnergyData)
admin.site.register(Anomaly)
admin.site.register(Notification)


