FROM python:3.12.1-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y  netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN pip install djangorestframework-simplejwt

# Créer un répertoire de travail
WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entrée

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
