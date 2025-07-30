import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from database import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or os.urandom(24)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# CSRF protection disabled - flask-wtf removed from requirements

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///lms.db")
# For Vercel, use PostgreSQL if available, otherwise fallback to SQLite
if not database_url.startswith(('postgresql://', 'postgres://')):
    database_url = "sqlite:///lms.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

def create_sample_data():
    """Create sample courses and users if database is empty"""
    import models
    
    # Clear existing data and recreate
    models.Course.query.delete()
    models.User.query.delete()
    db.session.commit()
    
    # Create sample users
    sample_users = [
        models.User(
            username="admin",
            email="admin@edutrack.com",
            first_name="Admin",
            last_name="User",
            role="admin"
        ),
        models.User(
            username="student",
            email="student@edutrack.com",
            first_name="John",
            last_name="Student",
            role="student"
        ),
        models.User(
            username="teacher",
            email="teacher@edutrack.com",
            first_name="Sarah",
            last_name="Johnson",
            role="teacher"
        )
    ]
    
    # Set passwords for users
    sample_users[0].set_password("admin123")
    sample_users[1].set_password("student123")
    sample_users[2].set_password("teacher123")
    
    # Add users to database
    for user in sample_users:
        db.session.add(user)
    db.session.commit()
    
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
            ),
            models.Course(
                title="Mobile App Development with React Native",
                description="Build cross-platform mobile applications using React Native and JavaScript.",
                instructor="Mr. Alex Thompson",
                duration_weeks=14,
                difficulty="Intermediate",
                max_students=18
            ),
            models.Course(
                title="Machine Learning Basics",
                description="Introduction to machine learning algorithms, data preprocessing, and model evaluation.",
                instructor="Dr. Maria Garcia",
                duration_weeks=12,
                difficulty="Advanced",
                max_students=12
            ),
            models.Course(
                title="Cybersecurity Fundamentals",
                description="Learn essential cybersecurity concepts, threat detection, and security best practices.",
                instructor="Prof. James Wilson",
                duration_weeks=10,
                difficulty="Intermediate",
                max_students=22
            ),
            models.Course(
                title="UI/UX Design Principles",
                description="Master user interface and user experience design principles and best practices.",
                instructor="Ms. Rachel Green",
                duration_weeks=8,
                difficulty="Beginner",
                max_students=25
            ),
            models.Course(
                title="Cloud Computing with AWS",
                description="Learn cloud computing fundamentals and AWS services for scalable applications.",
                instructor="Mr. Kevin Martinez",
                duration_weeks=12,
                difficulty="Intermediate",
                max_students=20
            ),
            models.Course(
                title="DevOps Fundamentals",
                description="Introduction to DevOps practices, CI/CD pipelines, and automation tools.",
                instructor="Dr. Amanda Foster",
                duration_weeks=10,
                difficulty="Advanced",
                max_students=18
            ),
            models.Course(
                title="Blockchain Development",
                description="Learn blockchain technology and smart contract development with Solidity.",
                instructor="Prof. Robert Chen",
                duration_weeks=14,
                difficulty="Advanced",
                max_students=15
            ),
            models.Course(
                title="Digital Marketing Strategy",
                description="Master digital marketing techniques, SEO, and social media marketing.",
                instructor="Ms. Jennifer Lee",
                duration_weeks=8,
                difficulty="Beginner",
                max_students=30
            ),
            models.Course(
                title="Project Management",
                description="Learn project management methodologies and tools for successful project delivery.",
                instructor="Mr. Thomas Anderson",
                duration_weeks=10,
                difficulty="Intermediate",
                max_students=25
            ),
            models.Course(
                title="Data Visualization",
                description="Create compelling data visualizations using tools like Tableau and D3.js.",
                instructor="Dr. Sarah Williams",
                duration_weeks=8,
                difficulty="Intermediate",
                max_students=20
            ),
            models.Course(
                title="Artificial Intelligence Basics",
                description="Introduction to AI concepts, neural networks, and machine learning applications.",
                instructor="Prof. Michael Brown",
                duration_weeks=12,
                difficulty="Advanced",
                max_students=16
            ),
            models.Course(
                title="Web Security",
                description="Learn web application security, vulnerability assessment, and penetration testing.",
                instructor="Mr. David Clark",
                duration_weeks=10,
                difficulty="Advanced",
                max_students=18
            ),
            models.Course(
                title="Mobile Game Development",
                description="Create mobile games using Unity and C# programming language.",
                instructor="Ms. Lisa Rodriguez",
                duration_weeks=16,
                difficulty="Intermediate",
                max_students=20
            ),
            models.Course(
                title="E-commerce Development",
                description="Build online stores and e-commerce platforms using modern web technologies.",
                instructor="Prof. Daniel Taylor",
                duration_weeks=12,
                difficulty="Intermediate",
                max_students=22
            ),
            models.Course(
                title="Content Creation",
                description="Learn content creation, video editing, and digital storytelling techniques.",
                instructor="Ms. Emily Davis",
                duration_weeks=8,
                difficulty="Beginner",
                max_students=28
            ),
            models.Course(
                title="Network Administration",
                description="Master network administration, configuration, and troubleshooting skills.",
                instructor="Mr. Christopher Wilson",
                duration_weeks=10,
                difficulty="Intermediate",
                max_students=20
            )
        ]
    
    # Assign some courses to the teacher
    teacher = models.User.query.filter_by(username='teacher').first()
    
    for i, course in enumerate(sample_courses):
        # Assign first 5 courses to the teacher
        if i < 5 and teacher:
            course.instructor_id = teacher.id
        db.session.add(course)
    db.session.commit()

def init_db():
    """Initialize database and create sample data"""
    with app.app_context():
        import models
        # Drop all tables and recreate them to ensure fresh schema
        db.drop_all()
        db.create_all()
        create_sample_data()

# Initialize database only when running locally
if __name__ == '__main__':
    init_db()

# Import route functions
from routes import index, register, login, logout, dashboard, courses, course_detail, enroll, grades, profile
from teacher_routes import teacher_dashboard, create_course, manage_course, grade_assignment, upload_material, create_announcement
from admin_routes import admin_dashboard, manage_users, edit_user, delete_user, manage_courses, edit_course, delete_course, system_analytics

# Register routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/courses', 'courses', courses)
app.add_url_rule('/course/<int:course_id>', 'course_detail', course_detail)
app.add_url_rule('/enroll/<int:course_id>', 'enroll', enroll)
app.add_url_rule('/grades', 'grades', grades)
app.add_url_rule('/profile', 'profile', profile)

# Database test route (for debugging)
@app.route('/test-db')
def test_db():
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return {'status': 'success', 'message': 'Database connected!', 'database_url': app.config["SQLALCHEMY_DATABASE_URI"]}
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'database_url': app.config["SQLALCHEMY_DATABASE_URI"]}

# Teacher routes
app.add_url_rule('/teacher/dashboard', 'teacher_dashboard', teacher_dashboard)
app.add_url_rule('/teacher/create-course', 'create_course', create_course, methods=['GET', 'POST'])
app.add_url_rule('/teacher/manage-course/<int:course_id>', 'manage_course', manage_course)
app.add_url_rule('/teacher/grade/<int:course_id>/<int:student_id>', 'grade_assignment', grade_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/upload-material/<int:course_id>', 'upload_material', upload_material, methods=['GET', 'POST'])
app.add_url_rule('/teacher/create-announcement/<int:course_id>', 'create_announcement', create_announcement, methods=['GET', 'POST'])

# Admin routes
app.add_url_rule('/admin/dashboard', 'admin_dashboard', admin_dashboard)
app.add_url_rule('/admin/manage-users', 'manage_users', manage_users)
app.add_url_rule('/admin/edit-user/<int:user_id>', 'edit_user', edit_user, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete-user/<int:user_id>', 'delete_user', delete_user)
app.add_url_rule('/admin/manage-courses', 'manage_courses', manage_courses)
app.add_url_rule('/admin/edit-course/<int:course_id>', 'edit_course', edit_course, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete-course/<int:course_id>', 'delete_course', delete_course)
app.add_url_rule('/admin/analytics', 'system_analytics', system_analytics)

if __name__ == '__main__':
    # Only enable debug mode in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
