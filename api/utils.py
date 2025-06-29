import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

def prepare_input_for_prediction(data_list, scaler, lookback=60):
    # Garante que cada item é um dicionário
    dicts = [d.dict() if hasattr(d, "dict") else d for d in data_list]
    df = pd.DataFrame(dicts)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    scaled = scaler.transform(df)
    X_input = np.expand_dims(scaled[-lookback:], axis=0)
    return X_input

def inverse_transform_close(predicted_scaled, scaler, close_index=3, total_features=5):
    zeros = np.zeros((len(predicted_scaled), total_features))
    zeros[:, close_index] = predicted_scaled.flatten()
    return scaler.inverse_transform(zeros)[:, close_index]

def fetch_latest_data(ticker: str, lookback: int = 60):
    df = yf.download(ticker, period=f"{lookback + 10}d", interval="1d")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns.name = None
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    return df[-lookback:], df.index[-1].date() if not df.empty else datetime.today().date()
