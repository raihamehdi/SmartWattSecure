# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
from django.shortcuts import render
from .arduino import get_mock_data

def dashboard(request):
    # Get the mock data
    data = get_mock_data()
    return render(request, 'dashboard.html', {'data': data})


from django.http import JsonResponse
from .models import EnergyData
from .arduino import get_mock_data

def update_energy_data(request):
    if request.method == 'GET':
        data = get_mock_data()  # Get mock data from arduino.py
        EnergyData.objects.create(
            voltage=data['voltage'],
            current=data['current'],
            power=data['power'],
            total_units_consumed=data['total_units_consumed']
        )
        return JsonResponse({'status': 'success', 'data': data})
    return JsonResponse({'status': 'failure'}, status=400)

from django.http import JsonResponse
from .models import EnergyData

def energy_data_api(request):
    data = EnergyData.objects.all().values('timestamp', 'voltage', 'current', 'power')
    return JsonResponse(list(data), safe=False)

from django.shortcuts import render

def dashboard2(request):
    return render(request, 'smartwatt/dashboard2.html')



