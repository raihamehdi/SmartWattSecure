from smartwatt.models import EnergyData
from smartwatt.arduino import get_mock_data, predict  


def handle(self, *args, **kwargs):
        
        voltage, current, power, total_units_consumed = get_mock_data()
        predictions = predict()
        
        
        EnergyData.objects.create(
            voltage=voltage,
            current=current,
            power=power,
            total_units_consumed=total_units_consumed,
            predictions=predictions
        )
        self.stdout.write(self.style.SUCCESS('Mock data updated successfully!'))
