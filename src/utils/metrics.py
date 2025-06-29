import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def mape(y_true, y_pred):
    """Erro percentual absoluto médio."""
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def calculate_metrics(y_true, y_pred):
    """Calcula MAE, RMSE e MAPE."""
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": root_mean_squared_error(y_true, y_pred),
        "MAPE": mape(y_true, y_pred)
    }

def print_metrics(metrics_dict, title=""):
    """Exibe as métricas de forma formatada."""
    if title:
        print(f"--- {title} ---")
    for key, value in metrics_dict.items():
        print(f"{key}: {value:.4f}")

def plot_predictions(y_true, y_pred, title="Comparação: Real vs Previsto"):
    """Plota série real e prevista lado a lado."""
    plt.figure(figsize=(12, 6))
    plt.plot(y_true, label="Real")
    plt.plot(y_pred, label="Previsto")
    plt.title(title)
    plt.xlabel("Período")
    plt.ylabel("Valor")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_series(data, title="Série Temporal", columns=None):
    """Plota a série temporal (pandas DataFrame)."""
    if columns:
        data = data[columns]
    data.plot(figsize=(12, 6), title=title)
    plt.xlabel("Data")
    plt.ylabel("Valor")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
