# Usa imagem base leve do Python 3.13
FROM python:3.13-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["uvicorn", "src.super_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
