from django.contrib import admin
from django.urls import path
from .views import registeradmin, signup, login, sendotp, verifyotp, index, home,energyc, resetpass


urlpatterns = [
    path('registeradmin', registeradmin, name='registeradmin'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('sendotp', sendotp, name='sendotp'),
    path('verifyotp', verifyotp, name='verifyotp'),
    path('', index, name='index'),
    path('home', home, name='home'),
    path('energyc', energyc, name='energyc'),
    path('resetpass', resetpass, name='resetpass'),
    
    
]