import numpy as np
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def load_scaler_from_data(df):
    scaler = MinMaxScaler()
    scaler.fit(df)
    return scaler

def prepare_input_sequence(df, lookback=60):
    scaler = load_scaler_from_data(df)
    scaled = scaler.transform(df)
    last_window = scaled[-lookback:]
    X_input = np.expand_dims(last_window, axis=0)
    return X_input, scaler

def fetch_latest_data(ticker: str, lookback: int = 60):
    df = yf.download(ticker, period=f"{lookback + 10}d", interval="1d")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns.name = None
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
    return df[-lookback:], df.index[-1]

def predict_next_close(ticker: str, target_date: str = None, model_dir: str = "models"):
    lookback = 60
    df, last_available_date = fetch_latest_data(ticker, lookback)

    if target_date:
        target_date_obj = datetime.strptime(target_date, "%Y-%m-%d").date()
        if target_date_obj > datetime.today().date() + timedelta(days=7):
            print(f"A data fornecida ({target_date}) está muito no futuro. Utilizando última data disponível: {last_available_date.date()}")
        prediction_date = min(target_date_obj, last_available_date.date())
    else:
        prediction_date = last_available_date.date()

    X_input, scaler = prepare_input_sequence(df, lookback)
    model = load_model(os.path.join(model_dir, f"lstm_model_{ticker}.h5"))
    y_pred_scaled = model.predict(X_input)

    close_index = list(df.columns).index('Close')
    n_features = df.shape[1]

    def reintegrate_column(column_values, column_index, total_columns):
        zeros_before = np.zeros((len(column_values), column_index))
        zeros_after = np.zeros((len(column_values), total_columns - column_index - 1))
        return np.concatenate([zeros_before, column_values.reshape(-1, 1), zeros_after], axis=1)

    y_pred_inv = scaler.inverse_transform(reintegrate_column(y_pred_scaled, close_index, n_features))[:, close_index]

    return y_pred_inv[0], prediction_date

if __name__ == "__main__":
    pred, date = predict_next_close("AAPL", target_date="2025-07-10")
    print(f"Preço previsto de fechamento para {date} - AAPL: ${pred:.2f}")
