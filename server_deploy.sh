#!/bin/sh
set -e

git pull
docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml exec python python manage.py migrate
docker compose -f docker-compose.prod.yml exec npm  sh -c "npm install && npm run build-no-tsc"
docker compose -f docker-compose.prod.yml exec python python manage.py collectstatic

touch curriculum-mapping-tool/wsgi.py