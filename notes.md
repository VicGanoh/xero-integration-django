# Docker commands
Part#1
docker build --tag python-django .
docker run --publish 8000:8000 python-django
Part#2
docker-compose build
docker-compose run --rm app django-admin startproject xero_integration.
docker-compose up