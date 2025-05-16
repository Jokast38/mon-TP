# Utilise une image officielle Python comme image de base
FROM python:3.11-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt ./

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port utilisé par Flask
EXPOSE 5000

# Définit la commande de démarrage du conteneur
CMD ["python", "app.py"]
