import pickle
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_svm.pkl')

def load_model():
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
        return model

def predict(X):
    model = load_model()
    predictions = model.predict(X)
    print("Predictions:", predictions)
    for prediction in predictions:
                if prediction == 1:
                    print("Your consumption is suspicious")
                else:
                    print("Your readings are normal")

if __name__ == '__main__':
    X_test = [[3.5, 240.0, 5.0],[1.7,240.0,5.7]]  
    predict(X_test)

