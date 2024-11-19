import serial
import pickle
import os
import time
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import collections

recent_data = collections.deque(maxlen=1440)  # Store up to 1440 recent points for a daily rolling average

def update_recent_data(new_data):
    recent_data.append(new_data)
recent_data = []  # Initialize as an empty list if it's not already defined

def compute_features(power):
    global recent_data
    recent_data.append(power)  # Assuming power is a valid numeric value to be added to the list

    # Ensure recent_data is a list and has sufficient length for slicing
    if isinstance(recent_data, list):
        # Compute lag_1 as the last value in recent_data, or use power if recent_data is empty
        lag_1 = recent_data[-1] if recent_data else power
        lag_1440 = recent_data[-14] if len(recent_data) >= 14 else power
        # Calculate the rolling average of the last 60 and 1440 data points
        rolling_avg_60 = sum(recent_data[-6:]) / min(len(recent_data), 6) if recent_data else power
        rolling_avg_1440 = sum(recent_data[-14:]) / min(len(recent_data), 14) if recent_data else power
    else:
        # If recent_data is not a list, handle the error
        lag_1, rolling_avg_60,lag_1440, rolling_avg_1440 = power, power, power, power  # Default values

    return lag_1, rolling_avg_60, lag_1440, rolling_avg_1440

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'logreg_model.pkl')
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
    X_df = pd.DataFrame(X, columns=[
    'Global_active_power', 'Voltage', 'Hour', 'DayOfWeek', 'Month',
    'lag_1', 'rolling_avg_60', 'lag_1440', 'rolling_avg_1440'])

    X_df = X_df.rename(columns={
        'power': 'Global_active_power',
        'voltage': 'Voltage',
        'hour': 'Hour',
        'day_of_week': 'DayOfWeek',
        'month': 'Month',
        'lag_1' :'lag_1',
        'rolling_avg_60' :'rolling_avg_60',
        'lag_1440' :'lag_1440',
        'rolling_avg_1440' : 'rolling_avg_1440'
        
    })
    X_scaled = scaler.transform(X_df)
    predictions = model.predict(X_scaled)
    return predictions

# Define a global list to store recent power values
recent_power_data = []

def data():
    ser = None
    try:
        ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=10)
        time.sleep(2)
        while True:
            raw_data = ser.readline().decode().strip()
            if raw_data:
                values = raw_data.split(',')
                if len(values) == 4:
                    voltage, current, power, energy = map(float, values)

                    # Update recent power data for feature calculations
                    recent_power_data.append(power)

                    # Keep recent_power_data limited to the last 1440 readings (or as needed)
                    if len(recent_power_data) > 1440:
                        recent_power_data.pop(0)

                    # Calculate additional features
                    lag_1 = recent_power_data[-1] if len(recent_power_data) >= 1 else power
                    rolling_avg_60 = sum(recent_power_data[-60:]) / min(len(recent_power_data), 60) if recent_power_data else power
                    lag_1440 = recent_power_data[-14] if len(recent_power_data) >= 14 else power  # Using 14 as discussed
                    rolling_avg_1440 = sum(recent_power_data[-14:]) / min(len(recent_power_data), 14) if recent_power_data else power

                    # Return the full set of values
                    if voltage > 0 and current > 0 and power > 0 and energy > 0:
                        return voltage, current, power, energy, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440
            time.sleep(1)
    except serial.SerialException as e:
        print("Serial Exception:", e)
    except Exception as e:
        print("General Exception:", e)
    finally:
        if ser and ser.is_open:
            ser.close()
    return None


if __name__ == '__main__':
        result = data()
        if result is not None:
            voltage, current, power, energy = data()
            now = datetime.now()
            hour = now.hour
            day_of_week = now.weekday()
            month = now.month
            
            update_recent_data(power)

            lag_1, rolling_avg_60, lag_1440, rolling_avg_1440 = compute_features(power)
            
            # Prepare the feature vector including lag and rolling features
            X_test = [[power, voltage, hour, day_of_week, month, lag_1, rolling_avg_60, lag_1440, rolling_avg_1440]]
            prediction = predict(X_test)
        else:
            print("Failed to retrieve data from Arduino.")
