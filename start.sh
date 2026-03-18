#!/usr/bin/env bash

# Exit on error
set -o errexit

python manage.py migrate
python manage.py seed_foods
python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
