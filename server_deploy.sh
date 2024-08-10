#!/bin/sh
set -e

git pull
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec python python manage.py migrate
docker compose -f docker-compose.prod.yml run --rm -it npm sh -c "npm install && npm run build"
docker compose -f docker-compose.prod.yml exec python python manage.py collectstatic --noinput --clear

# to restart the server https://stackoverflow.com/a/60833629/14324308
docker compose -f docker-compose.prod.yml exec python kill -HUP `ps -C gunicorn fch -o pid | head -n 1`