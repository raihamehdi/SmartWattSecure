import serial
import pickle
import os
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'svmver.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
ARDUINO_PORT = 'COM5'  
BAUD_RATE = 9600

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
    X_df = pd.DataFrame(X, columns=['power', 'voltage', 'hour', 'day_of_week', 'month'])
    X_scaled = scaler.transform(X_df)
    predictions = model.predict(X_scaled)
    return predictions

def data():
    ser = None
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=10)
        time.sleep(2)
        while True:
            data = ser.readline().decode().strip()
            if data:
                values = data.split(',')
                if len(values) == 4:
                    voltage, current, power, energy = map(float, values)
                    if voltage > 0 and current > 0 and power > 0 and energy > 0:
                        
                        return voltage, current, power, energy
            time.sleep(1) 
    except serial.SerialException:
        pass 
    except Exception:
        pass
    finally:
        if ser and ser.is_open:
            ser.close()  


if __name__ == '__main__':
    voltage, current, power, energy = data()
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    month = now.month

    X_test = [[power, voltage, hour, day_of_week, month]]
    prediction = predict(X_test)
