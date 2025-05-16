# Lony Platform

Plateforme éducative tout-en-un, développée avec Django + PostgreSQL + Docker.

## 📁 Structure du projet

renaissance/Lony
├── lony-backend/ # Backend Django avec CustomUser, UserProfile, JWT Auth
├── docker-compose.yml # Configuration Docker (backend + PostgreSQL)
└── README.md # Ce fichier



## 🚀 Démarrage rapide (via Docker)

```bash
# 1. Construire et démarrer les services
docker-compose up --build

# 2. Appliquer les migrations
docker-compose exec web python manage.py migrate

# 3. Créer un super utilisateur
docker-compose exec web python manage.py createsuperuser


📦 Fonctionnalités principales
✅ Authentification JWT (login, logout, refresh, verify)

✅ CustomUser avec rôles (admin, teacher, student)

✅ Gestion de profil avec avatar (UserProfile)

✅ Endpoints CRUD utilisateurs avec permissions par rôle

✅ PostgreSQL via Docker

🚧 Frontend à venir (ReactJS)

🛠️ Stack technique
Django / Django REST Framework

PostgreSQL

Docker

SimpleJWT