import numpy as np
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import ParameterGrid

def build_lstm_model(input_shape, units=50, optimizer='adam'):
    model = Sequential()
    model.add(LSTM(units, return_sequences=False, input_shape=input_shape))
    model.add(Dense(1))
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

def train_model(ticker: str, data_dir: str = "data/processed", save_dir: str = "models"):
    # Carregar dados
    X_train = np.load(os.path.join(data_dir, f"X_train_{ticker}.npy"))
    y_train = np.load(os.path.join(data_dir, f"y_train_{ticker}.npy"))

    # Espaço de busca dos hiperparâmetros
    param_grid = {
        'units': [32, 64],
        'optimizer': ['adam', 'rmsprop']
    }

    best_model = None
    best_loss = float("inf")
    best_params = None

    for params in ParameterGrid(param_grid):
        print(f"Treinando com params: {params}")
        model = build_lstm_model((X_train.shape[1], X_train.shape[2]), 
                                 units=params['units'], 
                                 optimizer=params['optimizer'])
        early_stopping = EarlyStopping(patience=5, restore_best_weights=True)
        history = model.fit(X_train, y_train, epochs=20, batch_size=32, 
                            validation_split=0.2, callbacks=[early_stopping], verbose=0)
        val_loss = min(history.history["val_loss"])
        print(f"Val Loss: {val_loss:.4f}")

        if val_loss < best_loss:
            best_loss = val_loss
            best_model = model
            best_params = params

    # Salvar o melhor modelo
    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, f"lstm_model_{ticker}.h5")
    best_model.save(model_path)

    print(f"Melhor modelo salvo em {model_path}")
    print(f"Hiperparâmetros ótimos: {best_params} | Val Loss: {best_loss:.4f}")

if __name__ == "__main__":
    train_model(ticker="AAPL")
