from django.urls import path
from django.contrib.auth.views import LogoutView
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
path('get_notifications/', views.get_notifications, name='get_notifications'),
path('today_anomaly/', views.get_today_anomalies, name='today_anomaly'),
path('get_notifications/', views.get_notifications, name='get_notifications'),
path('get_anomalies_data/weekly/', views.get_weekly_anomalies, name='get_weekly_anomalies'),
path('get_anomalies_data/monthly/',views.get_monthly_anomalies, name='get_monthly_anomalies'),
path('get_anomalies_data/yearly/', views.get_yearly_anomalies, name='get_yearly_anomalies'),
path('check/', views.check_and_create_anomaly, name='check'),
path('forgot-pass/', views.forgot_password_view, name='forgot-password'),  # Correct URL path for Forget Password pageath('forget-pass/', views.forgot_password_view, name='forget-pass'),
path('sendotp/', views.sendotp, name='sendotp'),
path('verifyotp/', views.verifyotp, name='verifyotp'),
path('resend-otp/', views.resend_otp, name='resend-otp'),  # Add the resend-otp URL
path('resetpass/', views.resetpass, name='resetpass'),
path('inquiry_view/',views.inquiry_view,name="inquiry_view"),
path('city-regions/', views.city_regions_view, name='city_regions_view'),
path('logoutt/', views.logout_admin, name='logoutt'),
path('delete_user/<int:user_id>/', views.delete_user_ajax, name='delete_user_ajax'),
path('admin-login/', views.admin_login, name='admin-login'),
path('restrict-user/<int:user_id>/', views.restrict_user, name='restrict_user'),
path('toggle-user-restriction/<int:user_id>/', views.toggle_user_restriction, name='toggle_user_restriction'),
path("mark_notification_read/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
path("unread_notifications_count/", views.unread_notification_count, name="unread_notifications_count"),
]

