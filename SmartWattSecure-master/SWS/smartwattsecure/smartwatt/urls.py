from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
path('signup/', views.signup, name='signup'),
path('login/', views.login, name='login'),
path('dashboard/', views.dashboard, name='dashboard'),
path('analytics/', views.analytics, name='analytics'),
path('dashboard/contact/', views.contact, name='contact'),
path('dashboard/help/', views.help, name='help'),
path('update/', views.update_energy_data, name='update_energy_data'),
path('api/energy_data/', views.energy_data_api, name='energy_data_api'),
path('api/monthly_data/', views.monthly_data, name='monthly_data'),
path('api/weekly_data/', views.weekly_data, name='weekly_data'),
<<<<<<< HEAD
path('get_anomalies/', views.get_anomalies, name='get_anomalies'),
path('get_notifications/', views.get_notifications, name='get_notifications'),
=======
path('update-user/', views.update_user, name='update_user'),
path('logout/', views.logout_view, name='logout')
>>>>>>> f61534a6dfe5d08f9429f0bc9964a6bf4efbb09d

]