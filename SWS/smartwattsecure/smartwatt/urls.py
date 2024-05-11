from django.contrib import admin
from django.urls import path
from .views import registeradmin,login


urlpatterns = [
    path('registeradmin', registeradmin, name='registeradmin'),
    path('login', login, name='login'),
    
]