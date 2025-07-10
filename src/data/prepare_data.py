import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os
import joblib


def download_and_prepare_data(ticker: str, start_date: str, end_date: str, lookback: int = 60, save_dir: str = "data/"):
    """
    Faz o download dos dados com yfinance e prepara os conjuntos X, y para LSTM multivariado.

    Parâmetros:
    - ticker: código da ação (ex: 'AAPL')
    - start_date: data de início (ex: '2020-01-01')
    - end_date: data de fim (ex: '2024-12-31')
    - lookback: quantidade de passos de tempo para o LSTM
    - save_dir: diretório onde os arquivos .npy serão salvos

    Saída:
    - None (salva X_train, X_test, y_train, y_test em arquivos)
    """

    print(f"Baixando dados de {ticker} de {start_date} a {end_date}...")
    df = yf.download(ticker, start=start_date, end=end_date)

    # Salvar dados brutos
    raw_dir = save_dir + "raw"
    os.makedirs(raw_dir, exist_ok=True)
    df.to_csv(os.path.join(raw_dir, f"{ticker}_{start_date}_{end_date}.csv"))

    # Remove nível do ticker se necessário
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns.name = None

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()

    # Normalização
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)
    scaler_path = os.path.join("models/", f"scaler_{ticker}.pkl")
    joblib.dump(scaler, scaler_path)    
    n_features = scaled.shape[1]

    # Criar janelas de tempo
    X, y = [], []
    for i in range(lookback, len(scaled)):
        X.append(scaled[i - lookback:i])
        y.append(scaled[i, df.columns.get_loc("Close")])
    X, y = np.array(X), np.array(y)

    # Dividir em treino e teste
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Garantir diretório
    proc_dir = save_dir + 'processed'
    os.makedirs(proc_dir, exist_ok=True)

    # Salvar os dados
    np.save(os.path.join(proc_dir, f"X_train_{ticker}.npy"), X_train)
    np.save(os.path.join(proc_dir, f"X_test_{ticker}.npy"), X_test)
    np.save(os.path.join(proc_dir, f"y_train_{ticker}.npy"), y_train)
    np.save(os.path.join(proc_dir, f"y_test_{ticker}.npy"), y_test)

    print(f"Dados salvos em {proc_dir}")

if __name__ == "__main__":
    # Exemplo de uso
    download_and_prepare_data(ticker="AAPL", start_date="2020-01-01", end_date="2024-12-31")
