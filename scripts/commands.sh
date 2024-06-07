#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

#Colocando o servidor pra rodar
echo "Coletando dados estaticos"
python manage.py collectstatic --noinput
echo "Preparando Migrações"
python manage.py makemigrations --noinput
echo "Realizando Migrações"
python manage.py migrate --noinput
echo "Iniciando Servidor"
python manage.py runserver 0.0.0.0:8000