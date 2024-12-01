# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Instalar dependências do sistema necessárias para PyTrustNFe e Git
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Atualizar pip para a versão mais recente
RUN pip install --upgrade pip

COPY requirements.txt .

# Instalar as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app/ ./app

# Expor a porta que a aplicação irá rodar
EXPOSE 5000

# Definir a variável de ambiente para produção
ENV FLASK_ENV=production

# Comando para iniciar a aplicação
CMD ["python", "app/main.py"]
