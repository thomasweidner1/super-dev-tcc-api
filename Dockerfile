# Usa a imagem oficial do Python 3.13
FROM python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas os arquivos de dependências primeiro (para aproveitar cache)
COPY requirements.txt .

# Instala dependências sem cache para reduzir tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta da aplicação (mesma do docker-compose)
EXPOSE 8000

# Comando padrão para rodar o backend (usando Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
