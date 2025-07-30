# EduTrack Vercel Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prerequisites
- [Git](https://git-scm.com/) installed on your computer
- [Vercel CLI](https://vercel.com/cli) (optional but recommended)
- A [GitHub](https://github.com) account
- A [Vercel](https://vercel.com) account

### 2. Prepare Your Project

#### Option A: Using Vercel CLI (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to your project directory**:
   ```bash
   cd EduTrack
   ```

4. **Deploy to Vercel**:
   ```bash
   vercel
   ```

5. **Follow the prompts**:
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `edutrack` (or your preferred name)
   - Directory: `./` (current directory)
   - Override settings: `N`

#### Option B: Using Vercel Dashboard (GitHub Integration)

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/edutrack.git
   git push -u origin main
   ```

2. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

3. **Click "New Project"**

4. **Import your GitHub repository**:
   - Select your `edutrack` repository
   - Framework Preset: `Other`
   - Root Directory: `./`
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: Leave empty

5. **Click "Deploy"**

### 3. Environment Variables (Optional)

If you want to use PostgreSQL instead of SQLite, add these environment variables in your Vercel dashboard:

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SESSION_SECRET`: A random secret key for sessions

### 4. Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## 📁 Project Structure

Your project is already configured for Vercel deployment with these key files:

- `main.py` - Entry point for Vercel
- `vercel.json` - Vercel configuration
- `requirements-vercel.txt` - Python dependencies
- `app.py` - Main Flask application

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "./main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/main.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production"
  }
}
```

### requirements-vercel.txt
```
flask==3.0.0
flask-sqlalchemy==3.1.1
werkzeug==3.0.1
psycopg2-binary==2.9.9
email-validator==2.1.0
```

## 🌐 Access Your Deployed App

After deployment, Vercel will provide you with:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: For each deployment

## 🔄 Updating Your App

### Using Vercel CLI:
```bash
vercel --prod
```

### Using GitHub Integration:
Simply push changes to your main branch, and Vercel will automatically redeploy.

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check that all dependencies are in `requirements-vercel.txt`
   - Ensure `main.py` exists and imports your app correctly

2. **Database Issues**:
   - Vercel uses serverless functions, so SQLite won't persist data
   - Consider using PostgreSQL or another cloud database

3. **Static Files Not Loading**:
   - Ensure static files are in the `static/` directory
   - Check that file paths are correct

4. **Routes Not Working**:
   - Verify that all routes are properly registered in `app.py`
   - Check the `vercel.json` routing configuration

### Debugging:

1. **Check Vercel Logs**:
   - Go to your project dashboard
   - Click on "Functions" to see serverless function logs

2. **Local Testing**:
   ```bash
   python main.py
   ```

## 📞 Support

If you encounter issues:
1. Check the [Vercel Documentation](https://vercel.com/docs)
2. Review the [Vercel Python Runtime](https://vercel.com/docs/runtimes#official-runtimes/python)
3. Check your project logs in the Vercel dashboard

## 🎉 Success!

Once deployed, your EduTrack application will be live at your Vercel URL with:
- ✅ Responsive design
- ✅ Interactive chatbot
- ✅ Course management system
- ✅ User authentication
- ✅ Admin and teacher dashboards
- ✅ Mobile-friendly interface

Your app is now ready for the world! 🌍 