# 🤖 src/ - Treinamento e Avaliação de Modelos

Este diretório contém os scripts principais para preparar dados, treinar modelos LSTM e avaliá-los com métricas de erro.

## 🔧 Scripts

- `data/prepare_data.py`: faz o download dos dados do yfinance, gera janelas temporais e normaliza os dados.
- `models/train.py`: treina um modelo LSTM multivariado com otimização de hiperparâmetros.
- `models/evaluate.py`: carrega o modelo treinado e calcula métricas como MAE, RMSE e MAPE.
- `inference/predict.py`: faz a inferência com novos dados, incluindo normalização e reversão do scaler.
- `utils/metrics.py`: funções utilitárias para cálculo de métricas e visualizações.

## 📦 Output esperado

- Arquivos `.npy` com dados normalizados para treino/teste
- Modelo treinado `.h5` e scaler `.pkl`
