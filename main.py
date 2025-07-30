from flask import Flask
from database import db
import os

# Create Flask app
app = Flask(__name__)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///lms.db")
if database_url.startswith(('postgresql://', 'postgres://')):
    database_url = "sqlite:///lms.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Now import the full app
from app import app as full_app

# Vercel handler
if __name__ != "__main__":
    # For Vercel deployment
    handler = full_app

# For local development
if __name__ == "__main__":
    full_app.run(debug=True)
