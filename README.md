# Projet de Scrapping et insertion de données dans une base de données

Ce projet implémente un script de scrapping pour collecter des données à partir de certains sites web et les insérer dans une base de données MySQL. Le script est écrit en Python et utilise Selenium pour le scrapping web, BeautifulSoup pour l'analyse HTML, et SQLAlchemy pour l'interaction avec la base de données.

## Utilisation

### Installation des dépendances
1. Cloner ce dépôt : `git clone https://github.com/votre-utilisateur/votre-projet.git`
2. Installer les dépendances Python : `pip install -r requirements.txt`

### Exécution du script
1. Assurez-vous d'avoir Docker installé sur votre système.
2. Construire l'image Docker : `docker build -t nom-image .`
3. Exécuter le conteneur Docker : `docker run -it nom-image`

## Structure des fichiers
- `scraper.py` : Le script Python principal pour le scrapping et l'insertion des données dans la base de données.
- `Dockerfile` : Le fichier Dockerfile pour la création de l'image Docker.
- `requirements.txt` : Le fichier contenant la liste des dépendances Python.