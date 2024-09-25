from django.contrib import admin
from django.urls import path
# from .views import SignUpView
from . import views
urlpatterns = [
# path('signup/', SignUpView.as_view(), name='signup'),
path('dashboard/', views.dashboard, name='dashboard'),
path('update/', views.update_energy_data, name='update_energy_data'),
path('api/energy_data/', views.energy_data_api, name='energy_data_api'),
path('dashboard2/', views.dashboard2, name='dashboard2'), 
path('index', views.index, name= 'index')
]