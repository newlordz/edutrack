# Database Setup for Vercel Deployment

## 🗄️ Database Options for Production

### **Option 1: PostgreSQL (Recommended)**

#### **Free PostgreSQL Providers:**

1. **Neon (Recommended)**
   - Free tier: 3GB storage, unlimited databases
   - Sign up: https://neon.tech
   - Get connection string like: `postgresql://user:password@host/database`

2. **Supabase**
   - Free tier: 500MB database, 50MB file storage
   - Sign up: https://supabase.com
   - Get connection string from dashboard

3. **Railway**
   - Free tier: $5 credit monthly
   - Sign up: https://railway.app
   - Easy PostgreSQL setup

#### **Setup Steps:**

1. **Create Database:**
   ```bash
   # Sign up for one of the providers above
   # Create a new PostgreSQL database
   # Copy the connection string
   ```

2. **Add Environment Variable in Vercel:**
   - Go to your Vercel project dashboard
   - Settings → Environment Variables
   - Add: `DATABASE_URL` = your PostgreSQL connection string

3. **Update requirements-vercel.txt:**
   ```
   flask==3.0.0
   flask-sqlalchemy==3.1.1
   werkzeug==3.0.1
   psycopg2-binary==2.9.9
   email-validator==2.1.0
   ```

### **Option 2: SQLite with External Storage**

#### **Using Cloud Storage (Advanced):**
- Store SQLite file in AWS S3, Google Cloud Storage, or similar
- Download on startup, upload on shutdown
- More complex but keeps SQLite

### **Option 3: Keep SQLite (Development Only)**

#### **For Testing/Demo:**
- Accept that data resets on each deployment
- Good for demos and testing
- Not suitable for production with real users

## 🔧 Database Migration Script

Create a script to initialize your PostgreSQL database:

```python
# db_migrate.py
import os
from app import app, db
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement

def migrate_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Add sample data
        create_sample_data()
        
        print("Database migration completed!")

if __name__ == "__main__":
    migrate_database()
```

## 🚀 Quick Setup Commands

### **For Neon Database:**

1. **Sign up at neon.tech**
2. **Create new project**
3. **Copy connection string**
4. **Add to Vercel environment variables:**
   ```
   DATABASE_URL=postgresql://user:password@host/database
   ```

### **For Supabase:**

1. **Sign up at supabase.com**
2. **Create new project**
3. **Go to Settings → Database**
4. **Copy connection string**
5. **Add to Vercel environment variables**

## 🔍 Testing Your Database Connection

Add this to your app.py for debugging:

```python
@app.route('/test-db')
def test_db():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        return {'status': 'success', 'message': 'Database connected!'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
```

## 📊 Database Schema

Your current models will work with PostgreSQL:

- **User** - Authentication and user management
- **Course** - Course information and metadata
- **Enrollment** - Student-course relationships
- **Grade** - Student performance tracking
- **CourseMaterial** - Course resources
- **Announcement** - Course announcements

## 🔄 Data Migration

If you have existing data:

1. **Export from SQLite:**
   ```bash
   sqlite3 lms.db ".dump" > backup.sql
   ```

2. **Import to PostgreSQL:**
   ```bash
   psql your_connection_string < backup.sql
   ```

## 🛡️ Security Considerations

1. **Environment Variables:**
   - Never commit database URLs to git
   - Use Vercel's environment variable system

2. **Connection Pooling:**
   - Your app already has connection pooling configured
   - Good for serverless environments

3. **Backup Strategy:**
   - Set up automated backups with your provider
   - Regular data exports

## 🎯 Recommended Setup for Production

1. **Use Neon PostgreSQL** (free, reliable)
2. **Set up environment variables in Vercel**
3. **Test database connection**
4. **Deploy and verify functionality**

## 🆘 Troubleshooting

### **Common Issues:**

1. **Connection Timeout:**
   - Check connection string format
   - Verify network access

2. **Permission Errors:**
   - Ensure database user has proper permissions
   - Check SSL requirements

3. **Migration Errors:**
   - Run migration script locally first
   - Check for syntax errors

### **Debug Commands:**

```bash
# Test local PostgreSQL connection
psql your_connection_string

# Check Vercel environment variables
vercel env ls

# View deployment logs
vercel logs
``` 