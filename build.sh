#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -o errexit  

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput
