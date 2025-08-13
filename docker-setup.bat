@echo off
REM Code Matrix Docker Setup Script for Windows
REM This script helps you get Code Matrix running with Docker on Windows

echo 🚀 Code Matrix Docker Setup
echo ==========================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Create environment file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment file...
    copy .env.docker .env
    echo ⚠️  Please edit .env file with your actual values (especially GEMINI_API_KEY)
)

REM Parse command line arguments
if "%1"=="build" goto build
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="shell" goto shell
if "%1"=="migrate" goto migrate
if "%1"=="admin" goto admin
if "%1"=="populate" goto populate
if "%1"=="test" goto test
if "%1"=="clean" goto clean
goto usage

:build
echo 🔨 Building Docker images...
docker-compose build
goto end

:up
echo 🚀 Starting Code Matrix...
docker-compose up -d
echo ✅ Code Matrix is running!
echo 🌐 Visit: http://localhost:8000
goto end

:down
echo 🛑 Stopping Code Matrix...
docker-compose down
goto end

:restart
echo 🔄 Restarting Code Matrix...
docker-compose down
docker-compose up -d
goto end

:logs
echo 📋 Showing logs...
docker-compose logs -f
goto end

:shell
echo 🐚 Opening Django shell...
docker-compose exec web python manage.py shell
goto end

:migrate
echo 📦 Running migrations...
docker-compose exec web python manage.py migrate
goto end

:admin
echo 👤 Creating superuser...
docker-compose exec web python manage.py createsuperuser
goto end

:populate
echo 📚 Populating database with problems...
docker-compose exec web python manage.py populate_problems
goto end

:test
echo 🧪 Running tests...
docker-compose exec web python manage.py test
goto end

:clean
echo 🧹 Cleaning up...
docker-compose down -v
docker system prune -f
goto end

:usage
echo.
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   build       Build Docker images
echo   up          Start all services
echo   down        Stop all services
echo   restart     Restart all services
echo   logs        Show logs
echo   shell       Open Django shell
echo   migrate     Run database migrations
echo   admin       Create superuser
echo   populate    Populate database with problems
echo   test        Run tests
echo   clean       Clean up containers and volumes
echo.

:end
