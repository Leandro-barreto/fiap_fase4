# 🌐 api/ - API RESTful com FastAPI

Esta pasta contém a aplicação FastAPI para servir o modelo LSTM como uma API de predição de preços.

## 🚀 Principais Features

- `GET /`: página interativa com formulário de ticker e data
- `POST /api/predict`: endpoint para previsão com base no ticker e (opcionalmente) em dados históricos
- `POST /api/predict/from_csv`: envia um arquivo CSV com dados históricos para previsão
- `GET /metrics`: endpoint de métricas Prometheus para monitoramento

## 🧩 Organização

- `main.py`: inicializa a API, inclui rotas, templates e monitoração
- `routes/predict.py`: define as rotas de predição
- `schemas.py`: modelos Pydantic para entrada e saída
- `utils.py`: pré-processamento e transformação dos dados
- `monitoring.py`: integra o Prometheus com FastAPI usando Instrumentator
- `static/home.html`: página HTML interativa com formulário para uso da API

## 📊 Monitoramento com Prometheus e Grafana

A API expõe métricas em tempo real através do endpoint `/metrics`, como:
- Tempo de resposta por rota
- Quantidade de requisições
- Status HTTP retornados

Essas métricas são consumidas pelo **Prometheus**, que faz a coleta periódica dos dados. O **Grafana**, por sua vez, é responsável por exibir visualizações personalizadas com essas informações.

### Relação:
- **Prometheus** coleta → `GET /metrics`
- **Grafana** consulta o Prometheus → cria painéis visuais e alertas

### 📈 Métricas exibidas no dashboard do Grafana:

- ⏱️ **Tempo médio de resposta**:
  - Query: `rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])`
  - Mostra o tempo médio que cada rota leva para responder, com base em uma janela de 1 minuto.

- 📈 **Taxa de requisições por segundo**:
  - Query: `rate(http_requests_total[1m])`
  - Quantas requisições estão sendo feitas por segundo para a API.

- 💾 **Uso de Memória RAM**:
  - Query: `process_resident_memory_bytes / 1024 / 1024`
  - Mede a quantidade de memória usada pelo processo Python que roda a API (em MB).

- 🔁 **CPU total do processo**:
  - Query: `process_cpu_seconds_total`
  - Tempo total de CPU usado pela API desde que iniciou (acumulado).

- 🚦 **Requisições por status HTTP**:
  - Query: `sum by (status) (rate(http_requests_total[1m]))`
  - Mostra a taxa de respostas por código de status HTTP (ex: 200, 404, 500).

## 🐳 Por que usar Docker Compose?

O `docker-compose.yml` é usado para orquestrar múltiplos serviços ao mesmo tempo:

- `api`: a aplicação FastAPI
- `prometheus`: coleta métricas da API
- `grafana`: visualiza essas métricas em dashboards

Ele permite:
- Subir tudo com um único comando: `docker-compose up`
- Compartilhar redes entre os serviços
- Configurar volumes e provisionamento automático de dashboards

## ▶️ Executar localmente

```bash
docker-compose up --build
```

Acesse:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (usuário: admin / senha: admin)
