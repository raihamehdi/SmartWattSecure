import random
import pickle
import os
import math

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_svm.pkl')

def get_mock_data():
    voltage = round(random.uniform(220, 240), 2)  
    current = round(random.uniform(0, 10), 2)     
    power = round(voltage * current, 2)
    reactive_power = round(math.sqrt(power), 2)           
    return {
        "voltage": voltage,
        "current": current,
        "power": power,
        "reactive_power":reactive_power,
        "total_units_consumed": round(power * random.uniform(0.1, 0.5), 2)  
    }
    
def load_model():
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
        return model

def predict(X):
    model = load_model()
    predictions = model.predict(X)
    return predictions            

if __name__ == '__main__':
    mock_data = get_mock_data()
    power = mock_data['power']
    reactive_power = mock_data['reactive_power']
    voltage = mock_data['voltage']
    X_test = [[power, reactive_power, voltage]]  
    predict(X_test)

