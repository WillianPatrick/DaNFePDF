# Usar uma imagem base oficial do Python
FROM python:3.9-slim

# Instalar dependências do sistema necessárias para PyTrustNFe e ReportLab
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    libffi-dev \
    libfreetype6 \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    zlib1g-dev \
    git \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Instalar fontes necessárias
RUN apt-get update && apt-get install -y \
    fonts-dejavu \
    fonts-liberation \
    fonts-freefont-ttf \
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
