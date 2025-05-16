#!/bin/sh
set -e

echo "⏳ Attente de la base de données ($DB_HOST:$DB_PORT)..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done

echo "✅ Base de données prête !"
python manage.py makemigrations
python manage.py migrate
echo "🚀 Démarrage du serveur Django..."
python manage.py runserver 0.0.0.0:8000
