# Vercel Deployment Guide for EduTrack

## Overview
This guide helps you deploy EduTrack to Vercel and troubleshoot common issues.

## Files Structure
- `main.py` - Vercel entry point
- `app.py` - Main Flask application
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

## Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Fix Vercel deployment issues"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Connect your GitHub repository to Vercel
   - Set the root directory to `EduTrack`
   - Deploy

## Environment Variables
Set these in Vercel dashboard:
- `FLASK_ENV=production`
- `SESSION_SECRET=your-secret-key-here`

## Troubleshooting

### Runtime Errors
If you get runtime errors:

1. **Check the logs** in Vercel dashboard
2. **Test locally** with `python main.py`
3. **Check database path** - should use `/tmp/lms.db` for Vercel

### Common Issues

1. **Import Errors**
   - All imports are now wrapped in try-catch blocks
   - Check if all required files are present

2. **Database Issues**
   - Database is stored in `/tmp` directory for Vercel
   - Visit `/init-db` to initialize the database
   - Visit `/test-db` to test database connection

3. **Route Errors**
   - All routes have fallback functions
   - Check if templates are present

## Testing Routes

After deployment, test these endpoints:

- `/health` - Basic health check
- `/test` - App status
- `/test-db` - Database connection test
- `/init-db` - Initialize database with sample data

## Local Development

```bash
cd EduTrack
python app.py
```

## Vercel Configuration

The `vercel.json` file:
- Points to `main.py` as the entry point
- Routes all requests to the Flask app
- Sets environment variables

## Database

- Uses SQLite for simplicity
- Database file: `/tmp/lms.db` (Vercel) or `lms.db` (local)
- Sample data is created when visiting `/init-db`

## Support

If issues persist:
1. Check Vercel logs for detailed error messages
2. Test each route individually
3. Verify all dependencies are in `requirements.txt` 