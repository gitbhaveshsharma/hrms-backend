# Deployment Guide - Railway

This guide will help you deploy the HRMS Lite backend to Railway.

## Prerequisites

1. A Railway account (https://railway.app)
2. Your Neon PostgreSQL database credentials
3. Git repository connected to Railway

## Deployment Steps

### 1. Set Up Railway Project

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your `hrms-backend` repository
4. Railway will automatically detect it as a Python project

### 2. Configure Environment Variables

In Railway dashboard, add these environment variables:

```env
DATABASE_URL=postgresql://neondb_owner:rkness-aiwkm6ff-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require

ENVIRONMENT=production

CORS_ORIGINS=https://your-frontend-url.com,http://localhost:3000

APP_TITLE=HRMS Lite API
APP_VERSION=1.0.0
APP_DESCRIPTION=Human Resource Management System API
```

**Important:** Update `CORS_ORIGINS` with your actual frontend URL once deployed.

### 3. Railway Configuration Files

The following files are already configured for Railway:

- **Procfile** - Tells Railway how to start the app
- **railway.json** - Railway-specific configuration
- **nixpacks.toml** - Build configuration
- **runtime.txt** - Python version specification
- **requirements.txt** - Python dependencies

### 4. Database Migrations

After first deployment:

1. Open Railway terminal (click on service → "Terminal" tab)
2. Run migrations:

   ```bash
   alembic upgrade head
   ```

3. (Optional) Seed sample data:
   ```bash
   python seed_data.py
   ```

### 5. Verify Deployment

Once deployed, Railway will provide a URL like: `https://your-app.railway.app`

Test endpoints:

- Health check: `https://your-app.railway.app/health`
- API docs: `https://your-app.railway.app/docs`
- Get employees: `https://your-app.railway.app/api/employees`

## Common Issues & Solutions

### Issue: "No start command was found"

**Solution:** This is fixed by the `Procfile`, `railway.json`, and `nixpacks.toml` files.

### Issue: Database connection errors

**Solution:**

- Ensure `DATABASE_URL` environment variable is set correctly in Railway
- Make sure Neon database is not paused
- Check that IP is allowed in Neon (Railway uses dynamic IPs, so allow all)

### Issue: Build fails

**Solution:**

- Check Railway build logs for specific errors
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility (3.14.0)

### Issue: App crashes after deployment

**Solution:**

- Check Railway deploy logs
- Ensure migrations are run: `alembic upgrade head`
- Verify all environment variables are set

## Performance Optimization

The app is configured with:

- **NullPool** for Neon serverless (no connection pooling overhead)
- **Fast connection timeouts** (5 seconds)
- **Efficient database queries** with proper indexing
- **Disabled SQL logging** in production

## Monitoring

Railway provides:

- **Logs**: View real-time application logs
- **Metrics**: CPU, memory, and network usage
- **Health checks**: Automatic health monitoring via `/health` endpoint

## Scaling

Railway automatically handles:

- Auto-scaling based on load
- Zero-downtime deployments
- SSL certificates
- CDN for static assets

## Support

If deployment issues persist:

1. Check Railway build/deploy logs
2. Review Neon database status
3. Verify all environment variables
4. Check the `/health` endpoint response

## Next Steps

After successful deployment:

1. Update frontend CORS origin
2. Run database migrations
3. Seed initial data (optional)
4. Test all API endpoints
5. Set up monitoring alerts
6. Configure custom domain (optional)

---

**Note:** The current Neon database URL is visible in environment variables. Make sure to keep it secure and rotate credentials if exposed.
