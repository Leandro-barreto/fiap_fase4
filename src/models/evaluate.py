import numpy as np
import os
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def evaluate_model(ticker: str, data_dir: str = "data/processed", model_dir: str = "models"):
    # Carregar dados e modelo
    X_test = np.load(os.path.join(data_dir, f"X_test_{ticker}.npy"))
    y_test = np.load(os.path.join(data_dir, f"y_test_{ticker}.npy"))
    model = load_model(os.path.join(model_dir, f"lstm_model_{ticker}.h5"))

    # Previsões
    y_pred = model.predict(X_test).flatten()

    # Métricas
    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    mape_val = mape(y_test, y_pred)

    print(f"Resultados para {ticker}:")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAPE: {mape_val:.2f}%")

if __name__ == "__main__":
    evaluate_model(ticker="AAPL")
