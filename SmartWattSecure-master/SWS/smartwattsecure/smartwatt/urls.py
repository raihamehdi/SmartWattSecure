from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
path('signup/', views.signup, name='signup'),
path('login/', views.login, name='login'),
path('dashboard/', views.dashboard, name='dashboard'),
path('dashboard/contact/', views.contact, name='contact'),
path('dashboard/help/', views.help, name='help'),
path('update/', views.update_energy_data, name='update_energy_data'),
path('api/energy_data/', views.energy_data_api, name='energy_data_api'),
path('api/units-consumed/', views.units_consumed_view, name='units_consumed_api')


]