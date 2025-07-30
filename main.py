from app import app, db, init_db

# Initialize database for Vercel
def init_vercel_db():
    try:
        with app.app_context():
            db.create_all()
            # Only create sample data if tables are empty
            from models import User
            if not User.query.first():
                from app import create_sample_data
                create_sample_data()
    except Exception as e:
        print(f"Database init error: {e}")

# Initialize database
init_vercel_db()

# Vercel handler
if __name__ != "__main__":
    # For Vercel deployment
    handler = app

# For local development
if __name__ == "__main__":
    app.run(debug=True)
