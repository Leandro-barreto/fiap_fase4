# Imagem base
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Copiar dependências
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código-fonte
COPY . .

# Expor a porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar a aplicação com Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
