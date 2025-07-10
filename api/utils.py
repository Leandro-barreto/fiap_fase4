import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta, date
from sklearn.preprocessing import MinMaxScaler

def prepare_input_for_prediction(data_list, lookback=60):
    dicts = [d.dict() if hasattr(d, "dict") else d for d in data_list]
    df = pd.DataFrame(dicts)
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    X_input = np.expand_dims(scaled[-lookback:], axis=0)

    return X_input, scaler

def inverse_transform_close(predicted_scaled, scaler, close_index=3, total_features=5):
    zeros = np.zeros((len(predicted_scaled), total_features))
    zeros[:, close_index] = predicted_scaled.flatten()
    return scaler.inverse_transform(zeros)[:, close_index]

def fetch_data(ticker: str, lookback: int = 60, end_date: date = None):
    start_date = end_date - timedelta(days=lookback + 10)
    df = yf.download(ticker, end=str(end_date), start=str(start_date))

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns.name = None

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    return df[-lookback:],  end_date
