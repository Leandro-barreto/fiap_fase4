# 🌐 api/ - API RESTful com FastAPI

Esta pasta contém a aplicação FastAPI para servir o modelo LSTM como uma API de predição de preços.

## 🚀 Principais Features

- `GET /`: página interativa com formulário de ticker e data
- `POST /api/predict`: endpoint para previsão com base no ticker e (opcionalmente) em dados históricos
- `GET /metrics`: métricas Prometheus para monitoramento

## 🧩 Organização

- `main.py`: inicializa a API, inclui rotas e monitoração
- `routes/predict.py`: define a rota de predição
- `schemas.py`: define os modelos Pydantic para validação de entrada/saída
- `utils.py`: normalização e utilitários de predição
- `monitoring.py`: integra Prometheus com FastAPI

## 📊 Monitoramento

- Integração com Prometheus (via `/metrics`)
- Painel Grafana customizado com métricas de latência e uso

Para rodar tudo:

```bash
docker-compose up --build
```
