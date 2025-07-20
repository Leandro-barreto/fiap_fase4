# 🤖 src/ - Treinamento e Avaliação de Modelos

Este diretório contém os scripts principais para preparar dados, treinar modelos LSTM e avaliá-los com métricas de erro.

## 🔧 Scripts

- `data/prepare_data.py`: faz o download dos dados do yfinance, gera janelas temporais e normaliza os dados.
- `models/train.py`: treina um modelo LSTM multivariado com otimização de hiperparâmetros.
- `models/evaluate.py`: carrega o modelo treinado e calcula métricas como MAE, RMSE e MAPE.
- `inference/predict.py`: faz a inferência com novos dados, incluindo normalização e reversão do scaler.
- `utils/metrics.py`: funções utilitárias para cálculo de métricas e visualizações.

## 🧠 Detalhes do modelo

- O modelo é um **LSTM multivariado** que considera as colunas: `Open`, `High`, `Low`, `Close`, `Volume`.
- Utiliza janelas temporais de 60 dias (`lookback = 60`) para prever o preço de fechamento do dia seguinte.
- Os dados são normalizados com `MinMaxScaler` e salvos em arquivos `.npy` para treino/teste.
- A separação entre treino e teste é **temporal**, com 80% dos dados para treino e 20% para teste.

## 🔍 Otimização de hiperparâmetros

Durante o treinamento, é realizado um `grid search` simples para encontrar a melhor combinação entre:
- `units`: número de unidades LSTM (`[32, 64]`)
- `optimizer`: algoritmo de otimização (`['adam', 'rmsprop']`)

O melhor modelo (menor `val_loss`) é salvo como arquivo `.h5`.

## 📦 Output esperado

- Arquivos `.npy` com dados normalizados para treino/teste
- Modelo treinado `.h5` em `models/`
- Scaler `.pkl` salvo para reutilização futura
