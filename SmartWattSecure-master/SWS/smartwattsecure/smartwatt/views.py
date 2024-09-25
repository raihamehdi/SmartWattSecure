from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import JsonResponse
from django.shortcuts import render
from .forms import CustomUserCreationForm
from .arduino import get_mock_data, predict
from .models import EnergyData
from datetime import datetime
from django.utils import timezone


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    
# def signup(request):
#     return render(request, signup.html)

def dashboard(request):
    if request.method == 'GET':
        data = EnergyData.objects.all()
        return render(request, 'dashboard.html', {'data': data})

def update_energy_data(request):
    if request.method == 'GET':
        data = get_mock_data()
        power = data['power']
        voltage = data['voltage']
        now = timezone.now()
        hour = now.hour  
        day_of_week = now.weekday()  
        month = now.month 
        X_test = [[power, voltage, hour, day_of_week, month]]

        # Get the actual prediction from the model
        predictions = predict(X_test)

        # Determine if the data is suspicious or normal based on the prediction
        if predictions[0] == 0:  # 'Normal' prediction
            prediction_result = "normal"
        elif predictions[0] == 1:  # 'High' prediction
            prediction_result = "high"
        else:  # 'Suspicious' prediction
            prediction_result = "suspicious"

        # Store the generated data and the prediction result in the database
        EnergyData.objects.create(
            current=data['current'],
            power=data['power'],
            voltage=data['voltage'],
            total_units_consumed=data['total_units_consumed'],
            prediction=prediction_result,
            timestamp=now
        )
        
        # Return the generated data and prediction result
        return JsonResponse({'data': data, 'predictions': prediction_result})
    return JsonResponse({'status': 'failure'}, status=400)



def energy_data_api(request):
    data = EnergyData.objects.all()
    return JsonResponse(list(data.values()), safe=False)


def dashboard2(request):
    update_energy_data(request)
    return render(request, 'dashboard2.html')

def index(request):
    return render(request, 'index.html')







