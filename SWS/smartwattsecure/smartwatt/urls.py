from django.contrib import admin
from django.urls import path
from .views import registeradmin,signup, login, send_otp


urlpatterns = [
    path('registeradmin', registeradmin, name='registeradmin'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('send_otp', send_otp, name='send_otp'),
    # path('verifyotp', verifyotp, name='verifyotp'),
    
    
]