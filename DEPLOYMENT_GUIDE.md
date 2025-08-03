# Code Matrix - Deployment Guide

## Phase 1: Production Deployment on Render

Your Code Matrix application is now ready for production deployment! Here's what has been configured:

### 🔥 What's Ready

1. **Production Dependencies Installed**:
   - `gunicorn`: Production-grade web server
   - `whitenoise`: Efficient static file serving
   - `dj-database-url`: PostgreSQL database configuration
   - `psycopg2-binary`: PostgreSQL driver

2. **Security & Production Settings**:
   - DEBUG mode disabled in production
   - SECRET_KEY loaded from environment variables
   - HTTPS redirect and security headers enabled
   - Static files optimized with compression

3. **Database Configuration**:
   - Automatic PostgreSQL database connection in production
   - Falls back to SQLite for local development

4. **Deployment Files Created**:
   - `Procfile`: Tells Render how to run the app
   - `build.sh`: Automated build and migration script
   - `render.yaml`: Complete deployment configuration
   - `runtime.txt`: Specifies Python 3.11.4

### 🚀 Deploy to Render (Free!)

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "feat: Add production deployment configuration"
git push origin master
```

#### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. This automatically connects your repositories

#### Step 3: Deploy Your App
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Online-Judge-Project`
3. Configure the service:
   - **Name**: `code-matrix`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn online_judge.wsgi:application`
   - **Plan**: Free

#### Step 4: Set Environment Variables
In the Render dashboard, add these environment variables:
- `DEBUG`: `false`
- `SECRET_KEY`: `your-super-secret-key-here` (generate a secure one)
- `GEMINI_API_KEY`: `your-gemini-api-key`

#### Step 5: Deploy!
Click "Deploy" and watch your app go live!

### 🎯 What You'll Get

- **Live URL**: `https://code-matrix.onrender.com` (or similar)
- **Free PostgreSQL Database**: Automatically provisioned
- **HTTPS**: Secure connection enabled
- **Auto-Deploy**: Updates when you push to GitHub (optional)

### 🔧 Testing Locally with Production Settings

To test your production configuration locally:

```bash
# Set environment variables
export DEBUG=false
export SECRET_KEY=your-secret-key
export GEMINI_API_KEY=your-api-key

# Test the production server locally
gunicorn online_judge.wsgi:application --bind 127.0.0.1:8000
```

### 📊 Monitoring & Next Steps

1. **Set up Uptime Monitoring**:
   - Create a free account on [uptimerobot.com](https://uptimerobot.com)
   - Add your Render URL for monitoring
   - Get alerts if your site goes down

2. **Performance Optimization**:
   - Monitor response times in Render dashboard
   - Check database query performance
   - Optimize static file loading

3. **Phase 2 Preparation**:
   - Your app is now ready for microservice architecture
   - Database is scalable PostgreSQL
   - Static files are optimized

### 🐛 Troubleshooting

**Common Issues:**
- **Build fails**: Check that all dependencies are in `requirements.txt`
- **Static files not loading**: Run `python manage.py collectstatic` locally first
- **Database errors**: Ensure migrations are up to date
- **AI features not working**: Verify `GEMINI_API_KEY` is set correctly

**Debug Mode:**
Never set `DEBUG=true` in production! For troubleshooting, check Render logs.

---

🎉 **Congratulations!** Your Code Matrix is production-ready!

Once deployed, you'll have a professional, scalable online judge platform with AI features running in the cloud for free.
