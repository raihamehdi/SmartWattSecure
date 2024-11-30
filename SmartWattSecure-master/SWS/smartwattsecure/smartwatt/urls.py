from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
path('signup/', views.signup, name='signup'),
path('login/', views.login, name='login'),
path('adminpanel/', views.adminview, name='adminview'),
path('dashboard/', views.dashboard, name='dashboard'),
path('analytics/', views.analytics, name='analytics'),
path('dashboard/contact/', views.contact, name='contact'),
path('dashboard/help/', views.help, name='help'),
path('api/energy_data/', views.energy_data_api, name='energy_data_api'),
path('api/yearly_data/', views.yearly_data, name='yearly_data'),
path('api/monthly_data/', views.monthly_data, name='monthly_data'),
path('api/weekly_data/', views.weekly_data, name='weekly_data'),
path('logout/', views.logout_view, name='logout'),
path('edit/username/', views.edit_username, name='edit_username'),
path('edit/email/', views.edit_email, name='edit_email'),
path('edit/password/', views.edit_password, name='edit_password'),
<<<<<<< HEAD
path('get_anomalies/', views.get_anomalies, name='get_anomalies'),
path('get_notifications/', views.get_notifications, name='get_notifications'),
=======
path('today_anomaly/', views.get_today_anomalies, name='today_anomaly'),
path('get_notifications/', views.get_notifications, name='get_notifications'),
path('get_anomalies_data/weekly/', views.get_weekly_anomalies, name='get_weekly_anomalies'),
path('get_anomalies_data/monthly/',views.get_monthly_anomalies, name='get_monthly_anomalies'),
path('get_anomalies_data/yearly/', views.get_yearly_anomalies, name='get_yearly_anomalies'),
path('check/', views.check_and_create_anomaly, name='check'),
path('sendotp/', views.sendotp, name='sendotp'),
path('verifyotp/', views.verifyotp, name='verifyotp'),
path('resetpass/', views.resetpass, name='resetpass'),
>>>>>>> 1083d61651b2e95a5235028e57632e001fb00b66

]