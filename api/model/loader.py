import os
from tensorflow.keras.models import load_model
import joblib

def load_model_and_scaler(ticker: str):
    model = load_model(f"models/lstm_model_{ticker}.h5")
    scaler = joblib.load(f"models/scaler_{ticker}.pkl")
    return model, scaler
