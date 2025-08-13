# Code Matrix Docker Testing Guide

## Prerequisites
- Docker Desktop installed
- Docker Compose v2.0+
- Git for version control

## Quick Test Commands

### 1. Build and Start Services
```bash
# Clone and navigate
git clone https://github.com/Kartikey-M/Online-Judge-Project.git
cd Online-Judge-Project

# Setup environment
cp .env.docker .env
# Edit .env with your GEMINI_API_KEY

# Start services
docker-compose up -d
```

### 2. Verify Services
```bash
# Check running containers
docker-compose ps

# View logs
docker-compose logs web
docker-compose logs db
```

### 3. Initialize Platform
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create admin user
docker-compose exec web python manage.py createsuperuser

# Populate problems
docker-compose exec web python manage.py populate_problems
```

### 4. Test Application
- Visit: http://localhost:8000
- Login with admin credentials
- Test problem submission
- Verify AI assistant functionality

### 5. Performance Testing
```bash
# Check resource usage
docker stats

# Test database connection
docker-compose exec web python manage.py dbshell

# Run Django tests
docker-compose exec web python manage.py test
```

### 6. Production Readiness
```bash
# Production check
docker-compose exec web python production_check.py

# System test
docker-compose exec web python system_test.py
```

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml
2. **Database connection**: Check DATABASE_URL in .env
3. **Static files**: Run collectstatic if needed
4. **Permissions**: Ensure Docker has file access

### Debug Commands
```bash
# View detailed logs
docker-compose logs -f --tail=50 web

# Enter container shell
docker-compose exec web bash

# Restart specific service
docker-compose restart web

# Reset everything
docker-compose down -v
docker-compose up --build
```

## Expected Results
- Web app accessible on http://localhost:8000
- Admin panel at http://localhost:8000/admin/
- 10 coding problems populated
- AI assistant functional with valid API key
- All tests passing
