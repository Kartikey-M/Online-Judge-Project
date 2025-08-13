#!/bin/bash

# Code Matrix Docker Setup Script
# This script helps you get Code Matrix running with Docker

set -e

echo "🚀 Code Matrix Docker Setup"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.docker .env
    echo "⚠️  Please edit .env file with your actual values (especially GEMINI_API_KEY)"
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build Docker images"
    echo "  up          Start all services"
    echo "  down        Stop all services"
    echo "  restart     Restart all services"
    echo "  logs        Show logs"
    echo "  shell       Open Django shell"
    echo "  migrate     Run database migrations"
    echo "  admin       Create superuser"
    echo "  populate    Populate database with problems"
    echo "  test        Run tests"
    echo "  clean       Clean up containers and volumes"
    echo ""
}

# Parse command line arguments
case "${1:-}" in
    "build")
        echo "🔨 Building Docker images..."
        docker-compose build
        ;;
    "up")
        echo "🚀 Starting Code Matrix..."
        docker-compose up -d
        echo "✅ Code Matrix is running!"
        echo "🌐 Visit: http://localhost:8000"
        ;;
    "down")
        echo "🛑 Stopping Code Matrix..."
        docker-compose down
        ;;
    "restart")
        echo "🔄 Restarting Code Matrix..."
        docker-compose down
        docker-compose up -d
        ;;
    "logs")
        echo "📋 Showing logs..."
        docker-compose logs -f
        ;;
    "shell")
        echo "🐚 Opening Django shell..."
        docker-compose exec web python manage.py shell
        ;;
    "migrate")
        echo "📦 Running migrations..."
        docker-compose exec web python manage.py migrate
        ;;
    "admin")
        echo "👤 Creating superuser..."
        docker-compose exec web python manage.py createsuperuser
        ;;
    "populate")
        echo "📚 Populating database with problems..."
        docker-compose exec web python manage.py populate_problems
        ;;
    "test")
        echo "🧪 Running tests..."
        docker-compose exec web python manage.py test
        ;;
    "clean")
        echo "🧹 Cleaning up..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        show_usage
        exit 1
        ;;
esac
