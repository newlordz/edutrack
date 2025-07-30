from flask import render_template, request, redirect, url_for, flash, session, current_app
from database import db
from models import User, Course, Enrollment, Grade
from datetime import datetime
import random
import re

def index():
    featured_courses = Course.query.limit(8).all()
    return render_template('index.html', courses=featured_courses)

def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Input validation
        if not all([username, email, first_name, last_name, password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        # Username validation
        if len(username) < 3 or len(username) > 20:
            flash('Username must be between 3 and 20 characters', 'danger')
            return render_template('register.html')
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            flash('Username can only contain letters, numbers, and underscores', 'danger')
            return render_template('register.html')
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address', 'danger')
            return render_template('register.html')
        
        # Name validation
        if len(first_name) < 2 or len(last_name) < 2:
            flash('First and last names must be at least 2 characters long', 'danger')
            return render_template('register.html')
        
        # Password validation
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration. Please try again.', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        # Input validation
        if not username or not password:
            flash('Username and password are required', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard', 'warning')
        return redirect(url_for('login'))
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('User not found. Please log in again.', 'warning')
            return redirect(url_for('login'))
        
        # Redirect based on user role
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            # Student dashboard
            enrolled_courses = user.enrollments
            
            # Get recent grades
            recent_grades = Grade.query.filter_by(user_id=user.id).order_by(Grade.graded_at.desc()).limit(5).all()
            
            # Calculate dashboard stats
            total_study_hours = len(enrolled_courses) * 20  # Estimate 20 hours per course
            completed_courses = len([e for e in user.enrollments if e.status == 'completed'])
            
            # Calculate average grade
            user_grades = Grade.query.filter_by(user_id=user.id).all()
            if user_grades:
                average_grade = round(sum(grade.score for grade in user_grades if grade.score is not None) / len(user_grades), 1)
            else:
                average_grade = 0.0
            
            # Get current date
            from datetime import datetime
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            
            return render_template('dashboard.html', 
                                 user=user, 
                                 enrolled_courses=enrolled_courses, 
                                 recent_grades=recent_grades,
                                 total_study_hours=total_study_hours,
                                 completed_courses=completed_courses,
                                 average_grade=average_grade,
                                 current_date=current_date)
    except Exception as e:
        flash('An error occurred while loading your dashboard.', 'danger')
        return redirect(url_for('index'))

def courses():
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of courses per page
    
    query = Course.query
    
    if search:
        query = query.filter(Course.title.contains(search) | Course.description.contains(search))
    
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    
    # Add pagination
    courses_pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    
    return render_template('courses.html', 
                         courses=courses_pagination.items, 
                         pagination=courses_pagination,
                         difficulties=difficulties, 
                         current_search=search, 
                         current_difficulty=difficulty)

def course_detail(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        
        # Check if user is enrolled
        enrolled = False
        progress = 0
        user = None
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            enrollment = Enrollment.query.filter_by(user_id=session['user_id'], course_id=course_id).first()
            enrolled = enrollment is not None
            progress = enrollment.progress if enrollment else 0
        
        return render_template('course_detail.html', course=course, enrolled=enrolled, progress=progress, user=user)
    except Exception as e:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses'))

def enroll(course_id):
    if 'user_id' not in session:
        flash('Please log in to enroll in courses', 'warning')
        return redirect(url_for('login'))
    
    try:
        course = Course.query.get_or_404(course_id)
        user_id = session['user_id']
        
        # Check if already enrolled
        existing_enrollment = Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existing_enrollment:
            flash('You are already enrolled in this course', 'info')
            return redirect(url_for('course_detail', course_id=course_id))
        
        # Check if course is full
        if course.is_full():
            flash('This course is full', 'danger')
            return redirect(url_for('course_detail', course_id=course_id))
        
        # Create enrollment
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        
        # Create some sample grades for the enrolled course
        sample_assignments = [
            ("Quiz 1", random.randint(75, 95)),
            ("Assignment 1", random.randint(80, 98)),
            ("Midterm Exam", random.randint(70, 90)),
            ("Project 1", random.randint(85, 100))
        ]
        
        for assignment_name, score in sample_assignments:
            grade = Grade(
                user_id=user_id,
                course_id=course_id,
                assignment_name=assignment_name,
                score=score,
                feedback=f"Good work on {assignment_name}!"
            )
            db.session.add(grade)
        
        # Set random progress
        enrollment.progress = random.randint(10, 85)
        
        db.session.commit()
        
        flash(f'Successfully enrolled in {course.title}!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred during enrollment. Please try again.', 'danger')
        return redirect(url_for('course_detail', course_id=course_id))

def grades():
    if 'user_id' not in session:
        flash('Please log in to view your grades', 'warning')
        return redirect(url_for('login'))
    
    try:
        user_id = session['user_id']
        user_grades = Grade.query.filter_by(user_id=user_id).order_by(Grade.graded_at.desc()).all()
        
        # Group grades by course
        grades_by_course = {}
        for grade in user_grades:
            course_title = grade.course.title
            if course_title not in grades_by_course:
                grades_by_course[course_title] = []
            grades_by_course[course_title].append(grade)
        
        # Calculate course averages
        course_averages = {}
        for course_title, course_grades in grades_by_course.items():
            scores = [g.score for g in course_grades if g.score is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            course_averages[course_title] = avg_score
        
        return render_template('grades.html', grades_by_course=grades_by_course, course_averages=course_averages)
    except Exception as e:
        flash('An error occurred while loading your grades.', 'danger')
        return redirect(url_for('dashboard'))

def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('User not found. Please log in again.', 'warning')
            return redirect(url_for('login'))
            
        enrolled_courses = user.get_enrolled_courses()
        total_grades = Grade.query.filter_by(user_id=user.id).count()
        
        # Calculate overall GPA
        all_scores = [grade.score for grade in user.grades if grade.score is not None]
        overall_gpa = sum(all_scores) / len(all_scores) if all_scores else 0
        
        return render_template('profile.html', user=user, enrolled_courses=enrolled_courses, 
                             total_grades=total_grades, overall_gpa=overall_gpa)
    except Exception as e:
        flash('An error occurred while loading your profile.', 'danger')
        return redirect(url_for('dashboard'))
