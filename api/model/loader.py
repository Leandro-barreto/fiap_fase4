import os
from tensorflow.keras.models import load_model
import joblib

def load_model_ticker(ticker: str):
    model = load_model(f"models/lstm_model_{ticker}.h5")
    return model
