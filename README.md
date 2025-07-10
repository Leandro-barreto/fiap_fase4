# 📈 Projeto de Previsão de Ações com LSTM

Este repositório implementa um pipeline completo de previsão de preços de ações usando redes neurais LSTM, com deploy em uma API RESTful com FastAPI e monitoramento via Prometheus + Grafana.

## 🔗 Acessos rápidos

- [API FastAPI](http://localhost:8000/)
- [Documentação Swagger](http://localhost:8000/docs)
- [Métricas Prometheus](http://localhost:8000/metrics)
- [Interface Prometheus](http://localhost:9090)
- [Dashboard Grafana](http://localhost:3000)
- [📂 README da API](./api/README.md)
- [🧠 README do Treinamento (src)](./src/README.md)

## 📁 Estrutura do Projeto

```
├── api/              # API FastAPI (rotas, templates e monitoramento)
├── src/              # Scripts de preparação, treinamento e avaliação de modelo
├── data/             # Dados raw e processados
├── models/           # Modelos treinados (.h5) e scalers (.pkl)
├── monitoring/       # Configurações do Prometheus e Grafana
├── requirements.txt  # Dependências do projeto
├── docker-compose.yml
└── Dockerfile
```
