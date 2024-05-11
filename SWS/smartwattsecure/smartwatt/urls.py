from django.contrib import admin
from django.urls import path
from .views import registeradmin


urlpatterns = [
    path('registeradmin', registeradmin, name='registeradmin'),
    
]