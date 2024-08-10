#!/bin/sh
set -e

git pull
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec python python manage.py migrate
docker compose -f docker-compose.prod.yml run --rm -it npm sh -c "npm install && npm run build"
docker compose -f docker-compose.prod.yml exec python python manage.py collectstatic --noinput --clear

# to restart the server https://stackoverflow.com/a/60833629/14324308 #single quotes matter here
docker compose -f docker-compose.prod.yml exec python sh -c 'kill -HUP `ps -C gunicorn fch -o pid | head -n 1`'