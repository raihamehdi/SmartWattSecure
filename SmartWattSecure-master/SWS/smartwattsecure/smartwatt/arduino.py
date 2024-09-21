import random
import pickle
import os
from sklearn.preprocessing import StandardScaler
import math
from datetime import datetime 

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'svmver.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

def get_mock_data():
    voltage = round(random.uniform(220, 240), 2)  
    current = round(random.uniform(0, 10), 2)    
    power = round((voltage * current)/1000, 2)   
    tuc = round(power * random.uniform(0.1, 0.5), 2)      
    return {
        "voltage": voltage,
        "current": current,
        "power": power,
        "total_units_consumed": tuc
    }

def load_scaler():
    with open(SCALER_PATH, 'rb') as file:
        scaler = pickle.load(file)
        return scaler

def load_model():
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
        return model 

def predict(X):
    model = load_model()
    scaler = load_scaler()
    X_scaled = scaler.transform(X)  # Apply same scaling as training
    predictions = model.predict(X_scaled)
    print(predictions)
    return predictions           

if __name__ == '__main__':
    mock_data = get_mock_data()
    power = mock_data['power']
    voltage = mock_data['voltage']
    now = datetime.now()
    hour = now.hour  
    day_of_week = now.weekday()  
    month = now.month  
    
    X_test = [[power, voltage, hour, day_of_week, month]]
    
    print(power)
    predict(X_test)

