import os
import logging
from flask import Flask, session, flash, redirect, url_for, send_file, abort
from database import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or os.urandom(24)
# Remove ProxyFix for Vercel compatibility
# app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# CSRF protection disabled - flask-wtf removed from requirements

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///lms.db")
# For Vercel, always use SQLite since PostgreSQL dependencies aren't available
if database_url.startswith(('postgresql://', 'postgres://')):
    # Use /tmp directory for Vercel serverless environment
    database_url = "sqlite:////tmp/lms.db"
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import models after db initialization to avoid circular imports
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement

def create_sample_data():
    """Create sample courses and users if database is empty"""
    # Check if we already have data
    if User.query.count() > 0:
        print("Sample data already exists, skipping...")
        return
    
    print("Creating sample users and courses...")
    
    # Create sample users
    sample_users = [
        User(
            username="admin",
            email="admin@edutrack.com",
            first_name="Admin",
            last_name="User",
            role="admin"
        ),
        User(
            username="student",
            email="student@edutrack.com",
            first_name="John",
            last_name="Student",
            role="student"
        ),
        User(
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
        Course(
            title="Introduction to Python Programming",
            description="Learn the fundamentals of Python programming including variables, data types, control structures, and functions.",
            instructor="Dr. Sarah Johnson",
            duration_weeks=8,
            difficulty="Beginner",
            max_students=30
        ),
        Course(
            title="Web Development with Flask",
            description="Build dynamic web applications using Flask framework, HTML, CSS, and JavaScript.",
            instructor="Prof. Michael Chen",
            duration_weeks=12,
            difficulty="Intermediate",
            max_students=25
        ),
        Course(
            title="Data Science Fundamentals",
            description="Introduction to data analysis, visualization, and machine learning concepts using Python.",
            instructor="Dr. Emily Rodriguez",
            duration_weeks=10,
            difficulty="Intermediate",
            max_students=20
        ),
        Course(
            title="Database Design and SQL",
            description="Learn database design principles, SQL queries, and database management systems.",
            instructor="Prof. David Kim",
            duration_weeks=6,
            difficulty="Beginner",
            max_students=35
        ),
        Course(
            title="Advanced JavaScript",
            description="Master advanced JavaScript concepts including ES6+, async programming, and modern frameworks.",
            instructor="Ms. Lisa Wang",
            duration_weeks=8,
            difficulty="Advanced",
            max_students=15
        ),
        Course(
            title="Mobile App Development with React Native",
            description="Build cross-platform mobile applications using React Native and JavaScript.",
            instructor="Mr. Alex Thompson",
            duration_weeks=14,
            difficulty="Intermediate",
            max_students=18
        ),
        Course(
            title="Machine Learning Basics",
            description="Introduction to machine learning algorithms, data preprocessing, and model evaluation.",
            instructor="Dr. Maria Garcia",
            duration_weeks=12,
            difficulty="Advanced",
            max_students=12
        ),
        Course(
            title="Cybersecurity Fundamentals",
            description="Learn essential cybersecurity concepts, threat detection, and security best practices.",
            instructor="Prof. James Wilson",
            duration_weeks=10,
            difficulty="Intermediate",
            max_students=22
        ),
        Course(
            title="UI/UX Design Principles",
            description="Master user interface and user experience design principles and best practices.",
            instructor="Ms. Rachel Green",
            duration_weeks=8,
            difficulty="Beginner",
            max_students=25
        ),
        Course(
            title="Cloud Computing with AWS",
            description="Learn cloud computing fundamentals and AWS services for scalable applications.",
            instructor="Mr. Kevin Martinez",
            duration_weeks=12,
            difficulty="Intermediate",
            max_students=20
        ),
        Course(
            title="DevOps Fundamentals",
            description="Introduction to DevOps practices, CI/CD pipelines, and automation tools.",
            instructor="Dr. Amanda Foster",
            duration_weeks=10,
            difficulty="Advanced",
            max_students=18
        ),
        Course(
            title="Blockchain Development",
            description="Learn blockchain technology and smart contract development with Solidity.",
            instructor="Prof. Robert Chen",
            duration_weeks=14,
            difficulty="Advanced",
            max_students=15
        ),
        Course(
            title="Digital Marketing Strategy",
            description="Master digital marketing techniques, SEO, and social media marketing.",
            instructor="Ms. Jennifer Lee",
            duration_weeks=8,
            difficulty="Beginner",
            max_students=30
        ),
        Course(
            title="Project Management",
            description="Learn project management methodologies and tools for successful project delivery.",
            instructor="Mr. Thomas Anderson",
            duration_weeks=10,
            difficulty="Intermediate",
            max_students=25
        ),
        Course(
            title="Data Visualization",
            description="Create compelling data visualizations using tools like Tableau and D3.js.",
            instructor="Dr. Sarah Williams",
            duration_weeks=8,
            difficulty="Intermediate",
            max_students=20
        ),
        Course(
            title="Artificial Intelligence Basics",
            description="Introduction to AI concepts, neural networks, and machine learning applications.",
            instructor="Prof. Michael Brown",
            duration_weeks=12,
            difficulty="Advanced",
            max_students=16
        ),
        Course(
            title="Web Security",
            description="Learn web application security, vulnerability assessment, and penetration testing.",
            instructor="Mr. David Clark",
            duration_weeks=10,
            difficulty="Advanced",
            max_students=18
        ),
        Course(
            title="Mobile Game Development",
            description="Create mobile games using Unity and C# programming language.",
            instructor="Ms. Lisa Rodriguez",
            duration_weeks=16,
            difficulty="Intermediate",
            max_students=20
        ),
        Course(
            title="E-commerce Development",
            description="Build online stores and e-commerce platforms using modern web technologies.",
            instructor="Prof. Daniel Taylor",
            duration_weeks=12,
            difficulty="Intermediate",
            max_students=22
        ),
        Course(
            title="Content Creation",
            description="Learn content creation, video editing, and digital storytelling techniques.",
            instructor="Ms. Emily Davis",
            duration_weeks=8,
            difficulty="Beginner",
            max_students=28
        ),
        Course(
            title="Network Administration",
            description="Master network administration, configuration, and troubleshooting skills.",
            instructor="Mr. Christopher Wilson",
            duration_weeks=10,
            difficulty="Intermediate",
            max_students=20
        )
    ]
    
    # Assign some courses to the teacher
    teacher = User.query.filter_by(username='teacher').first()
    
    for i, course in enumerate(sample_courses):
        # Assign first 5 courses to the teacher
        if i < 5 and teacher:
            course.instructor_id = teacher.id
        db.session.add(course)
    db.session.commit()

def init_db():
    """Initialize database and create sample data only if needed"""
    with app.app_context():
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            # Only create tables if they don't exist
            print("Creating database tables...")
            db.create_all()
            print("Creating sample data...")
            create_sample_data()
        else:
            print("Database tables already exist, skipping initialization")
            # Check if we have any users
            try:
                user_count = User.query.count()
                if user_count == 0:
                    print("No users found, creating sample data...")
                    create_sample_data()
                else:
                    print(f"Database already has {user_count} users, skipping sample data creation")
            except Exception as e:
                print(f"Error checking existing data: {e}")
                # If there's an error, create tables anyway
                db.create_all()
                create_sample_data()

# Import route functions
try:
    from routes import index, register, login, logout, dashboard, courses, course_detail, enroll_course, study_material, mark_complete, submit_assignment, view_grades, profile, create_quiz, take_quiz, quiz_results, request_account_deletion, settings, certificates, schedule
    print("✓ Routes imported successfully")
except Exception as e:
    print(f"✗ Routes import failed: {e}")
    # If routes import fails, the app will crash - this is intentional
    # to prevent running with broken routes
    raise e

try:
    from teacher_routes import teacher_dashboard, create_course as teacher_create_course, manage_course, grade_assignment, upload_material, create_announcement, create_assignment, view_submissions, unenroll_student, unenroll_all_students, delete_course, request_course_deletion, manage_quizzes, quiz_results_overview, edit_quiz_answers, delete_quiz, manage_assignments, edit_assignment, delete_assignment, toggle_assignment_status, assignment_analytics
    print("✓ Teacher routes imported successfully")
except Exception as e:
    print(f"✗ Teacher routes import failed: {e}")
    # Create dummy functions
    def teacher_dashboard(): return "Teacher routes not available"
    def teacher_create_course(): return "Teacher routes not available"
    def manage_course(course_id): return "Teacher routes not available"
    def grade_assignment(submission_id): return "Teacher routes not available"
    def upload_material(course_id): return "Teacher routes not available"
    def create_announcement(course_id): return "Teacher routes not available"
    def create_assignment(course_id): return "Teacher routes not available"
    def view_submissions(assignment_id): return "Teacher routes not available"
    def unenroll_student(course_id, student_id): return "Teacher routes not available"
    def unenroll_all_students(course_id): return "Teacher routes not available"
    def delete_course(course_id): return "Teacher routes not available"
    def request_course_deletion(course_id): return "Teacher routes not available"
    def manage_quizzes(course_id): return "Teacher routes not available"
    def quiz_results_overview(quiz_id): return "Teacher routes not available"
    def edit_quiz_answers(quiz_id): return "Teacher routes not available"
    def delete_quiz(quiz_id): return "Teacher routes not available"
    def manage_assignments(course_id): return "Teacher routes not available"
    def edit_assignment(assignment_id): return "Teacher routes not available"
    def delete_assignment(assignment_id): return "Teacher routes not available"
    def toggle_assignment_status(assignment_id): return "Teacher routes not available"
    def assignment_analytics(assignment_id): return "Teacher routes not available"

try:
    from admin_routes import admin_dashboard, manage_users, edit_user, delete_user, manage_courses, create_course as admin_create_course, edit_course, delete_course, system_analytics, manage_deletion_requests, review_deletion_request, manage_user_deletion_requests, review_user_deletion_request
    print("✓ Admin routes imported successfully")
except Exception as e:
    print(f"✗ Admin routes import failed: {e}")
    # Create dummy functions
    def admin_dashboard(): return "Admin routes not available"
    def manage_users(): return "Admin routes not available"
    def edit_user(user_id): return "Admin routes not available"
    def delete_user(user_id): return "Admin routes not available"
    def manage_courses(): return "Admin routes not available"
    def admin_create_course(): return "Admin routes not available"
    def edit_course(course_id): return "Admin routes not available"
    def delete_course(course_id): return "Admin routes not available"
    def system_analytics(): return "Admin routes not available"
    def manage_deletion_requests(): return "Admin routes not available"
    def review_deletion_request(request_id): return "Admin routes not available"
    def manage_user_deletion_requests(): return "Admin routes not available"
    def review_user_deletion_request(request_id): return "Admin routes not available"

# Register routes
app.add_url_rule('/', 'index', index)
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', logout)
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/courses', 'courses', courses)
app.add_url_rule('/course/<int:course_id>', 'course_detail', course_detail)
app.add_url_rule('/enroll/<int:course_id>', 'enroll_course', enroll_course)
app.add_url_rule('/study/<int:material_id>', 'study_material', study_material)
app.add_url_rule('/study/<int:material_id>/complete', 'mark_complete', mark_complete, methods=['POST'])
app.add_url_rule('/submit/<int:assignment_id>', 'submit_assignment', submit_assignment, methods=['GET', 'POST'])
app.add_url_rule('/grades', 'view_grades', view_grades)
app.add_url_rule('/profile', 'profile', profile, methods=['GET', 'POST'])

# Settings, certificates, and schedule routes
app.add_url_rule('/settings', 'settings', settings, methods=['GET', 'POST'])
app.add_url_rule('/certificates', 'certificates', certificates)
app.add_url_rule('/schedule', 'schedule', schedule)

# Quiz routes
app.add_url_rule('/quiz/create/<int:course_id>', 'create_quiz', create_quiz, methods=['GET', 'POST'])
app.add_url_rule('/quiz/<int:quiz_id>/take', 'take_quiz', take_quiz, methods=['GET', 'POST'])
app.add_url_rule('/quiz/results/<int:attempt_id>', 'quiz_results', quiz_results)

# User account routes
app.add_url_rule('/account/request-deletion', 'request_account_deletion', request_account_deletion, methods=['GET', 'POST'])

# Simple test route
@app.route('/test')
def test():
    return {'status': 'success', 'message': 'App is running!'}

# Health check route (no database required)
@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'EduTrack is running!'}

# Database test route (for debugging)
@app.route('/test-db')
def test_db():
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        
        # Test if we can write to the database
        from models import User
        user_count = User.query.count()
        
        return {
            'status': 'success', 
            'message': 'Database connected and readable!', 
            'database_url': app.config["SQLALCHEMY_DATABASE_URI"],
            'user_count': user_count,
            'database_path': app.config["SQLALCHEMY_DATABASE_URI"]
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'database_url': app.config["SQLALCHEMY_DATABASE_URI"]}

# Enrollment test route (for debugging)
@app.route('/test-enrollment/<int:course_id>')
def test_enrollment(course_id):
    if 'user_id' not in session:
        return {'status': 'error', 'message': 'Not logged in'}
    
    try:
        from models import User, Course, Enrollment
        user = User.query.get(session['user_id'])
        course = Course.query.get(course_id)
        
        if not user or not course:
            return {'status': 'error', 'message': 'User or course not found'}
        
        # Check enrollment
        enrollment = Enrollment.query.filter_by(
            user_id=user.id,
            course_id=course_id
        ).first()
        
        # Check all enrollments for this course
        all_enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        return {
            'status': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            },
            'course': {
                'id': course.id,
                'title': course.title,
                'max_students': course.max_students
            },
            'enrollment': {
                'exists': enrollment is not None,
                'id': enrollment.id if enrollment else None,
                'status': enrollment.status if enrollment else None
            },
            'course_enrollments': len(all_enrollments),
            'all_enrollments': [{'user_id': e.user_id, 'status': e.status} for e in all_enrollments]
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Reset database route (for development only)
@app.route('/reset-db')
def reset_db():
    """Reset database - WARNING: This will delete all data!"""
    if os.environ.get('FLASK_ENV') == 'production':
        return {'status': 'error', 'message': 'Database reset not allowed in production'}
    
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            create_sample_data()
        return {'status': 'success', 'message': 'Database reset successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Database initialization route (for Vercel deployment)
@app.route('/init-db')
def init_db_route():
    try:
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            # Check if we have any users
            user_count = User.query.count()
            if user_count == 0:
                create_sample_data()
                return {'status': 'success', 'message': 'Database initialized with sample data!', 'user_count': User.query.count()}
            else:
                return {'status': 'success', 'message': 'Database already initialized!', 'user_count': user_count}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Teacher routes
app.add_url_rule('/teacher/dashboard', 'teacher_dashboard', teacher_dashboard)
app.add_url_rule('/teacher/create-course', 'teacher_create_course', teacher_create_course, methods=['GET', 'POST'])
app.add_url_rule('/teacher/manage-course/<int:course_id>', 'manage_course', manage_course)
app.add_url_rule('/teacher/upload-material/<int:course_id>', 'upload_material', upload_material, methods=['GET', 'POST'])
app.add_url_rule('/teacher/create-assignment/<int:course_id>', 'create_assignment', create_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/grade-submission/<int:submission_id>', 'grade_assignment', grade_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/grade-course/<int:course_id>/<int:student_id>', 'grade_course_assignment', grade_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/view-submissions/<int:assignment_id>', 'view_submissions', view_submissions)
app.add_url_rule('/teacher/create-announcement/<int:course_id>', 'create_announcement', create_announcement, methods=['GET', 'POST'])
app.add_url_rule('/teacher/unenroll-student/<int:course_id>/<int:student_id>', 'unenroll_student', unenroll_student)
app.add_url_rule('/teacher/unenroll-all-students/<int:course_id>', 'unenroll_all_students', unenroll_all_students, methods=['POST'])
app.add_url_rule('/teacher/request-course-deletion/<int:course_id>', 'request_course_deletion', request_course_deletion, methods=['GET', 'POST'])
app.add_url_rule('/teacher/delete-course/<int:course_id>', 'delete_course', delete_course, methods=['GET', 'POST'])

# Assignment management routes
app.add_url_rule('/teacher/manage-assignments/<int:course_id>', 'manage_assignments', manage_assignments)
app.add_url_rule('/teacher/edit-assignment/<int:assignment_id>', 'edit_assignment', edit_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/delete-assignment/<int:assignment_id>', 'delete_assignment', delete_assignment, methods=['GET', 'POST'])
app.add_url_rule('/teacher/toggle-assignment-status/<int:assignment_id>', 'toggle_assignment_status', toggle_assignment_status)
app.add_url_rule('/teacher/assignment-analytics/<int:assignment_id>', 'assignment_analytics', assignment_analytics)

# Quiz management routes
app.add_url_rule('/teacher/manage-quizzes/<int:course_id>', 'manage_quizzes', manage_quizzes)
app.add_url_rule('/teacher/quiz-results/<int:quiz_id>', 'quiz_results_overview', quiz_results_overview)
app.add_url_rule('/teacher/edit-quiz-answers/<int:quiz_id>', 'edit_quiz_answers', edit_quiz_answers, methods=['GET', 'POST'])
app.add_url_rule('/teacher/delete-quiz/<int:quiz_id>', 'delete_quiz', delete_quiz, methods=['GET', 'POST'])

# Admin routes
app.add_url_rule('/admin/dashboard', 'admin_dashboard', admin_dashboard)
app.add_url_rule('/admin/users', 'manage_users', manage_users)
app.add_url_rule('/admin/users/<int:user_id>/edit', 'edit_user', edit_user, methods=['GET', 'POST'])
app.add_url_rule('/admin/users/<int:user_id>/delete', 'delete_user', delete_user)
app.add_url_rule('/admin/courses', 'manage_courses', manage_courses)
app.add_url_rule('/admin/courses/<int:course_id>/edit', 'edit_course', edit_course, methods=['GET', 'POST'])
app.add_url_rule('/admin/courses/<int:course_id>/delete', 'delete_course', delete_course)
app.add_url_rule('/admin/create-course', 'admin_create_course', admin_create_course, methods=['GET', 'POST'])
app.add_url_rule('/admin/deletion-requests', 'manage_deletion_requests', manage_deletion_requests)
app.add_url_rule('/admin/deletion-requests/<int:request_id>/review', 'review_deletion_request', review_deletion_request, methods=['GET', 'POST'])
app.add_url_rule('/admin/user-deletion-requests', 'manage_user_deletion_requests', manage_user_deletion_requests)
app.add_url_rule('/admin/user-deletion-requests/<int:request_id>/review', 'review_user_deletion_request', review_user_deletion_request, methods=['GET', 'POST'])
app.add_url_rule('/admin/analytics', 'system_analytics', system_analytics)

# File serving route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    from flask import send_from_directory
    upload_dir = os.path.join(app.root_path, 'uploads')
    
    # Check if uploads directory exists
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
    
    return send_from_directory(upload_dir, filename)

# Debug route to check uploads directory
@app.route('/debug/uploads')
def debug_uploads():
    """Debug route to check uploads directory"""
    upload_dir = os.path.join(app.root_path, 'uploads')
    
    if not os.path.exists(upload_dir):
        return {'status': 'error', 'message': 'Uploads directory does not exist', 'path': upload_dir}
    
    try:
        files = os.listdir(upload_dir)
        file_info = []
        for filename in files:
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_info.append({
                    'filename': filename,
                    'size': os.path.getsize(file_path),
                    'path': file_path,
                    'exists': True
                })
        
        return {
            'status': 'success',
            'upload_dir': upload_dir,
            'exists': True,
            'files': file_info,
            'file_count': len(files)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'upload_dir': upload_dir}

# Debug route to check course materials
@app.route('/debug/materials')
def debug_materials():
    """Debug route to check course materials in database"""
    try:
        from models import CourseMaterial, Course
        
        materials = CourseMaterial.query.all()
        material_info = []
        
        for material in materials:
            # Check if file exists
            file_exists = False
            if material.file_path:
                full_path = os.path.join(app.root_path, material.file_path)
                file_exists = os.path.exists(full_path)
            
            material_info.append({
                'id': material.id,
                'title': material.title,
                'file_path': material.file_path,
                'file_type': material.file_type,
                'file_exists': file_exists,
                'course_id': material.course_id,
                'course_title': material.course.title if material.course else 'Unknown'
            })
        
        return {
            'status': 'success',
            'materials': material_info,
            'total_materials': len(materials)
        }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Download course material route
@app.route('/download-material/<int:material_id>')
def download_material(material_id):
    """Download course material files"""
    if 'user_id' not in session:
        flash('Please log in to download materials', 'warning')
        return redirect(url_for('login'))
    
    from models import CourseMaterial, Enrollment
    
    material = CourseMaterial.query.get_or_404(material_id)
    course = material.course
    
    # Check if user is enrolled or is the instructor
    user_id = session['user_id']
    user_role = session.get('role')
    
    if user_role == 'teacher' and material.course.instructor_id == user_id:
        # Teacher can download their own materials
        pass
    elif user_role == 'student':
        # Check if student is enrolled
        enrollment = Enrollment.query.filter_by(
            user_id=user_id,
            course_id=course.id
        ).first()
        if not enrollment:
            flash('You must be enrolled in this course to download materials', 'danger')
            return redirect(url_for('course_detail', course_id=course.id))
    else:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))
    
    if not material.file_path:
        flash('This material has no file attached', 'warning')
        return redirect(url_for('study_material', material_id=material_id))
    
    try:
        file_path = os.path.join(app.root_path, material.file_path)
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('study_material', material_id=material_id))
        
        return send_file(file_path, as_attachment=True, download_name=os.path.basename(material.file_path))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('study_material', material_id=material_id))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True, host='0.0.0.0', port=5001)
