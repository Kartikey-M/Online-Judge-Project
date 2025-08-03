#!/bin/bash

echo "Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Make and run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Build completed successfully!"
