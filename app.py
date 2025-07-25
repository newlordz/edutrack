import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///lms.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Create sample courses if none exist
    if models.Course.query.count() == 0:
        sample_courses = [
            models.Course(
                title="Introduction to Python Programming",
                description="Learn the fundamentals of Python programming including variables, data types, control structures, and functions.",
                instructor="Dr. Sarah Johnson",
                duration_weeks=8,
                difficulty="Beginner",
                max_students=30
            ),
            models.Course(
                title="Web Development with Flask",
                description="Build dynamic web applications using Flask framework, HTML, CSS, and JavaScript.",
                instructor="Prof. Michael Chen",
                duration_weeks=12,
                difficulty="Intermediate",
                max_students=25
            ),
            models.Course(
                title="Data Science Fundamentals",
                description="Introduction to data analysis, visualization, and machine learning concepts using Python.",
                instructor="Dr. Emily Rodriguez",
                duration_weeks=10,
                difficulty="Intermediate",
                max_students=20
            ),
            models.Course(
                title="Database Design and SQL",
                description="Learn database design principles, SQL queries, and database management systems.",
                instructor="Prof. David Kim",
                duration_weeks=6,
                difficulty="Beginner",
                max_students=35
            ),
            models.Course(
                title="Advanced JavaScript",
                description="Master advanced JavaScript concepts including ES6+, async programming, and modern frameworks.",
                instructor="Ms. Lisa Wang",
                duration_weeks=8,
                difficulty="Advanced",
                max_students=15
            )
        ]
        
        for course in sample_courses:
            db.session.add(course)
        db.session.commit()

# Import and register routes
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
