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

# Create superuser if environment variables are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput
    echo "Superuser created successfully!"
else
    echo "Superuser environment variables not set. Skipping superuser creation."
fi

echo "Build completed successfully!"
