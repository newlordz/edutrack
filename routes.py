from flask import render_template, request, redirect, url_for, flash, session
from app import app
from database import db
from models import User, Course, Enrollment, Grade
from datetime import datetime
import random

@app.route('/')
def index():
    featured_courses = Course.query.limit(3).all()
    return render_template('index.html', courses=featured_courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
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
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    enrolled_courses = user.get_enrolled_courses()
    
    # Get recent grades
    recent_grades = Grade.query.filter_by(user_id=user.id).order_by(Grade.graded_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', user=user, enrolled_courses=enrolled_courses, recent_grades=recent_grades)

@app.route('/courses')
def courses():
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', '')
    
    query = Course.query
    
    if search:
        query = query.filter(Course.title.contains(search) | Course.description.contains(search))
    
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    
    courses_list = query.all()
    difficulties = ['Beginner', 'Intermediate', 'Advanced']
    
    return render_template('courses.html', courses=courses_list, difficulties=difficulties, 
                         current_search=search, current_difficulty=difficulty)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Check if user is enrolled
    enrolled = False
    progress = 0
    if 'user_id' in session:
        enrollment = Enrollment.query.filter_by(user_id=session['user_id'], course_id=course_id).first()
        enrolled = enrollment is not None
        progress = enrollment.progress if enrollment else 0
    
    return render_template('course_detail.html', course=course, enrolled=enrolled, progress=progress)

@app.route('/enroll/<int:course_id>')
def enroll(course_id):
    if 'user_id' not in session:
        flash('Please log in to enroll in courses', 'warning')
        return redirect(url_for('login'))
    
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

@app.route('/grades')
def grades():
    if 'user_id' not in session:
        flash('Please log in to view your grades', 'warning')
        return redirect(url_for('login'))
    
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

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    enrolled_courses = user.get_enrolled_courses()
    total_grades = Grade.query.filter_by(user_id=user.id).count()
    
    # Calculate overall GPA
    all_scores = [grade.score for grade in user.grades if grade.score is not None]
    overall_gpa = sum(all_scores) / len(all_scores) if all_scores else 0
    
    return render_template('profile.html', user=user, enrolled_courses=enrolled_courses, 
                         total_grades=total_grades, overall_gpa=overall_gpa)
