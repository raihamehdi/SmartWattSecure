import random

def get_mock_data():
    # Simulate readings for voltage, current, and power
    voltage = round(random.uniform(220, 240), 2)  # Simulate voltage between 220V and 240V
    current = round(random.uniform(0, 10), 2)     # Simulate current between 0A and 10A
    power = round(voltage * current, 2)           # Calculate power
    return {
        "voltage": voltage,
        "current": current,
        "power": power,
        "total_units_consumed": round(power * random.uniform(0.1, 0.5), 2)  # Mock for total kWh
    }
    
