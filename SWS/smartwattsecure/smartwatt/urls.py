from django.contrib import admin
from django.urls import path
from .views import registeradmin, signup, login, sendotp, verifyotp, index


urlpatterns = [
    path('registeradmin', registeradmin, name='registeradmin'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('sendotp', sendotp, name='sendotp'),
    path('verifyotp', verifyotp, name='verifyotp'),
    path('', index, name='index'),
    
    
]