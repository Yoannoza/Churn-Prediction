# Utilise une image Python officielle comme base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de ton application dans le conteneur
COPY . /app

# Installe les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose le port 8000 pour FastAPI
EXPOSE 8000

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
