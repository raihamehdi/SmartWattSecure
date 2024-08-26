import pickle
import os

# Define the path to your model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_svm.pkl')

# Load the model
def load_model():
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
        print("Model loaded successfully.")
        return model
    

# Function to make predictions
def predict(X):
    model = load_model()
    predictions = model.predict(X)
    print("Predictions:", predictions)
    for prediction in predictions:
                if prediction == 1:
                    print("suspicious")
                else:
                    print("normal")
        

# Example usage
if __name__ == '__main__':
    X_test = [[5.0, 240.0, 5.0]]  # Replace with your actual input data
    predict(X_test)
