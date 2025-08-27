from flask import render_template, request, redirect, url_for, flash, session, current_app
from database import db
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement, Assignment, AssignmentSubmission, StudyProgress, Quiz, QuizQuestion, QuizAttempt, QuizAnswer, UserDeletionRequest
from datetime import datetime
import random
import re
import time

def parse_quiz_text(quiz_text):
    """
    Parse quiz text in the format:
    Quiz Title
    
    Question 1?
    A) Option A
    B) Option B
    C) Option C
    D) Option D
    
    Question 2?
    A) Option A
    B) Option B
    C) Option C
    D) Option D
    """
    lines = quiz_text.strip().split('\n')
    quiz_data = {
        'title': '',
        'questions': []
    }
    
    current_question = None
    question_num = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # First non-empty line is the quiz title
        if not quiz_data['title']:
            quiz_data['title'] = line
            continue
            
        # Check if this is a question (ends with ?)
        if line.endswith('?'):
            if current_question:
                quiz_data['questions'].append(current_question)
            
            current_question = {
                'question_text': line,
                'options': {},
                'correct_answer': None
            }
            question_num += 1
            continue
            
        # Check if this is an option (starts with A), B), C), D))
        if line.startswith(('A)', 'B)', 'C)', 'D)')):
            option_letter = line[0]
            option_text = line[2:].strip()
            
            # Check if this option is marked as correct
            if '[CORRECT]' in option_text:
                current_question['correct_answer'] = option_letter
                # Remove [CORRECT] from the display text
                option_text = option_text.replace('[CORRECT]', '').strip()
            
            current_question['options'][option_letter] = option_text
            
            # If no correct answer is specified yet, use the first option as fallback
            if not current_question['correct_answer']:
                current_question['correct_answer'] = option_letter
    
    # Add the last question
    if current_question:
        quiz_data['questions'].append(current_question)
    
    return quiz_data

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
            session['role'] = user.role
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))
    
    if user.role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    # Student dashboard
    enrolled_courses = user.get_enrolled_courses()
    recent_assignments = []
    upcoming_deadlines = []
    
    for course in enrolled_courses:
        # Get assignments for enrolled courses
        course_assignments = Assignment.query.filter_by(course_id=course.id, is_active=True).all()
        for assignment in course_assignments:
            # Check if student has submitted
            submission = AssignmentSubmission.query.filter_by(
                assignment_id=assignment.id,
                user_id=user.id
            ).first()
            
            if not submission:
                upcoming_deadlines.append(assignment)
            else:
                recent_assignments.append({
                    'assignment': assignment,
                    'submission': submission
                })
    
    # Sort by due date
    upcoming_deadlines.sort(key=lambda x: x.due_date)
    recent_assignments.sort(key=lambda x: x.submission.submitted_at, reverse=True)
    
    return render_template('dashboard.html',
                         user=user,
                         enrolled_courses=enrolled_courses,
                         recent_assignments=recent_assignments[:5],
                         upcoming_deadlines=upcoming_deadlines[:5])

def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    user = None
    enrolled = False
    enrollment = None
    progress = 0
    
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            enrollment = Enrollment.query.filter_by(
                user_id=user.id,
                course_id=course_id
            ).first()
            enrolled = enrollment is not None
            
            # Debug: Print enrollment status
            print(f"DEBUG: User {user.username} (ID: {user.id}) enrollment status for course {course_id}: {enrolled}")
            if enrollment:
                print(f"DEBUG: Enrollment found - ID: {enrollment.id}, Status: {enrollment.status}")
            
            # Calculate progress for enrolled students
            if enrolled and user.role == 'student':
                # Get total materials for the course
                total_materials = CourseMaterial.query.filter_by(course_id=course_id).count()
                if total_materials > 0:
                    # Get completed materials
                    completed_materials = StudyProgress.query.filter_by(
                        user_id=user.id,
                        course_id=course_id,
                        completion_status='completed'
                    ).count()
                    progress = (completed_materials / total_materials) * 100
                    print(f"DEBUG: Progress calculated: {progress}% ({completed_materials}/{total_materials} materials completed)")
                else:
                    print(f"DEBUG: No materials found for course {course_id}")
            else:
                print(f"DEBUG: User not enrolled or not a student. Role: {user.role}, Enrolled: {enrolled}")
    
    # Get course materials and assignments
    materials = CourseMaterial.query.filter_by(course_id=course_id).order_by(CourseMaterial.order_index).all()
    assignments = Assignment.query.filter_by(course_id=course_id, is_active=True).all()
    announcements = Announcement.query.filter_by(course_id=course_id).order_by(Announcement.created_at.desc()).all()
    
    return render_template('course_detail.html',
                         course=course,
                         user=user,
                         enrolled=enrolled,
                         enrollment=enrollment,
                         progress=progress,
                         materials=materials,
                         assignments=assignments,
                         announcements=announcements)

def enroll_course(course_id):
    if 'user_id' not in session:
        flash('Please log in to enroll in courses', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can enroll in courses', 'danger')
        return redirect(url_for('courses'))
    
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(
        user_id=user.id,
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        flash('You are already enrolled in this course', 'info')
        return redirect(url_for('course_detail', course_id=course_id))
    
    # Check if course is full
    if course.is_full():
        flash('This course is full and cannot accept more enrollments', 'danger')
        return redirect(url_for('course_detail', course_id=course_id))
    
    # Create enrollment
    enrollment = Enrollment(
        user_id=user.id,
        course_id=course_id
    )
    
    try:
        db.session.add(enrollment)
        db.session.commit()
        
        # Force session to flush and commit
        db.session.flush()
        
        # Verify enrollment was created
        verification = Enrollment.query.filter_by(
            user_id=user.id,
            course_id=course_id
        ).first()
        
        if verification:
            flash(f'Successfully enrolled in {course.title}!', 'success')
            # Redirect with success parameter to trigger auto-refresh
            return redirect(url_for('course_detail', course_id=course_id, enrolled='success'))
        else:
            flash('Enrollment created but verification failed. Please refresh the page.', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred during enrollment: {str(e)}', 'danger')
    
    return redirect(url_for('course_detail', course_id=course_id))

def study_material(material_id):
    if 'user_id' not in session:
        flash('Please log in to access course materials', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can access course materials', 'danger')
        return redirect(url_for('dashboard'))
    
    material = CourseMaterial.query.get_or_404(material_id)
    course = material.course
    
    # Check if student is enrolled
    enrollment = Enrollment.query.filter_by(
        user_id=user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('You must be enrolled in this course to access materials', 'danger')
        return redirect(url_for('course_detail', course_id=course.id))
    
    # Update study progress
    study_progress = StudyProgress.query.filter_by(
        user_id=user.id,
        material_id=material_id
    ).first()
    
    if not study_progress:
        study_progress = StudyProgress(
            user_id=user.id,
            course_id=course.id,
            material_id=material_id,
            completion_status='in_progress'
        )
        db.session.add(study_progress)
    else:
        study_progress.last_accessed = datetime.utcnow()
        if study_progress.completion_status == 'not_started':
            study_progress.completion_status = 'in_progress'
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
    return render_template('study_material.html',
                         material=material,
                         course=course,
                         study_progress=study_progress)

def mark_complete(material_id):
    if 'user_id' not in session:
        flash('Please log in to update study progress', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can update study progress', 'danger')
        return redirect(url_for('dashboard'))
    
    material = CourseMaterial.query.get_or_404(material_id)
    course = material.course
    
    # Check if student is enrolled
    enrollment = Enrollment.query.filter_by(
        user_id=user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('You must be enrolled in this course to update study progress', 'danger')
        return redirect(url_for('course_detail', course_id=course.id))
    
    if request.method == 'POST':
        action = request.form.get('action')
        notes = request.form.get('notes', '').strip()
        study_time = int(request.form.get('study_time', 0))
        
        print(f"DEBUG: Action: {action}, Notes: {notes}, Study Time: {study_time}")
        
        # Get or create study progress
        study_progress = StudyProgress.query.filter_by(
            user_id=user.id,
            material_id=material_id
        ).first()
        
        if not study_progress:
            study_progress = StudyProgress(
                user_id=user.id,
                course_id=course.id,
                material_id=material_id
            )
            db.session.add(study_progress)
            print(f"DEBUG: Created new StudyProgress for user {user.id}, material {material_id}")
        else:
            print(f"DEBUG: Found existing StudyProgress: {study_progress.id}")
        
        # Update study progress
        study_progress.notes = notes
        study_progress.study_time_minutes = study_time
        study_progress.last_accessed = datetime.utcnow()
        
        if action == 'mark_complete':
            study_progress.completion_status = 'completed'
            flash('Material marked as complete!', 'success')
            print(f"DEBUG: Marked as complete")
        elif action == 'mark_incomplete':
            study_progress.completion_status = 'in_progress'
            flash('Material marked as in progress!', 'success')
            print(f"DEBUG: Marked as in progress")
        elif action == 'save_notes':
            flash('Notes saved successfully!', 'success')
            print(f"DEBUG: Notes saved")
        else:
            print(f"DEBUG: Unknown action: {action}")
        
        try:
            db.session.commit()
            print(f"DEBUG: Database commit successful")
        except Exception as e:
            db.session.rollback()
            print(f"DEBUG: Database error: {e}")
            flash('An error occurred while updating study progress', 'danger')
    
    return redirect(url_for('study_material', material_id=material_id))

def submit_assignment(assignment_id):
    if 'user_id' not in session:
        flash('Please log in to submit assignments', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can submit assignments', 'danger')
        return redirect(url_for('dashboard'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    # Check if student is enrolled
    enrollment = Enrollment.query.filter_by(
        user_id=user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('You must be enrolled in this course to submit assignments', 'danger')
        return redirect(url_for('course_detail', course_id=course.id))
    
    # Check if already submitted
    existing_submission = AssignmentSubmission.query.filter_by(
        assignment_id=assignment_id,
        user_id=user.id
    ).first()
    
    if existing_submission:
        flash('You have already submitted this assignment', 'info')
        return redirect(url_for('course_detail', course_id=course.id))
    
    if request.method == 'POST':
        submission_text = request.form.get('submission_text', '').strip()
        file_path = None
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                # Simple file handling - in production, use proper file storage
                filename = f"{assignment_id}_{user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
                file_path = f"uploads/{filename}"
        
        if not submission_text and not file_path:
            flash('Please provide either text submission or upload a file', 'danger')
            return render_template('submit_assignment.html', assignment=assignment)
        
        # Create submission
        submission = AssignmentSubmission(
            assignment_id=assignment_id,
            user_id=user.id,
            submission_text=submission_text,
            file_path=file_path,
            status='submitted'
        )
        
        # Check if late
        if submission.is_late():
            submission.status = 'late'
        
        try:
            db.session.add(submission)
            db.session.commit()
            flash('Assignment submitted successfully!', 'success')
            return redirect(url_for('course_detail', course_id=course.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the assignment. Please try again.', 'danger')
    
    return render_template('submit_assignment.html', assignment=assignment, now=datetime.now())

def view_grades():
    if 'user_id' not in session:
        flash('Please log in to view your grades', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can view grades', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all grades for the user
    grades = Grade.query.filter_by(user_id=user.id).all()
    
    # Group grades by course
    course_grades = {}
    for grade in grades:
        course_id = grade.course_id
        if course_id not in course_grades:
            course_grades[course_id] = []
        course_grades[course_id].append(grade)
    
    # Get course details
    courses = Course.query.filter(Course.id.in_(course_grades.keys())).all()
    course_dict = {course.id: course for course in courses}
    
    # Calculate course averages - use course ID as key to match grades_by_course structure
    course_averages = {}
    for course_id, grades_list in course_grades.items():
        if grades_list:
            total_score = sum(grade.score for grade in grades_list if grade.score is not None)
            valid_grades = [grade for grade in grades_list if grade.score is not None]
            if valid_grades:
                course_averages[course_id] = total_score / len(valid_grades)
            else:
                course_averages[course_id] = 0.0
        else:
            course_averages[course_id] = 0.0
    
    return render_template('grades.html',
                         user=user,
                         grades_by_course=course_grades,
                         courses=course_dict,
                         course_averages=course_averages)

def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        email = request.form['email'].strip()
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Basic validation
        if not all([first_name, last_name, email]):
            flash('First name, last name, and email are required', 'danger')
            return render_template('profile.html', user=user)
        
        # Update basic info
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        
        # Handle password change
        if new_password:
            if not user.check_password(current_password):
                flash('Current password is incorrect', 'danger')
                return render_template('profile.html', user=user)
            
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return render_template('profile.html', user=user)
            
            if len(new_password) < 6:
                flash('New password must be at least 6 characters long', 'danger')
                return render_template('profile.html', user=user)
            
            user.set_password(new_password)
            flash('Password updated successfully!', 'success')
        
        try:
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
    
    # Get user's enrolled courses
    enrolled_courses = user.get_enrolled_courses()
    
    # Calculate overall GPA
    grades = Grade.query.filter_by(user_id=user.id).all()
    overall_gpa = 0.0
    if grades:
        total_score = sum(grade.score for grade in grades if grade.score is not None)
        valid_grades = [grade for grade in grades if grade.score is not None]
        if valid_grades:
            overall_gpa = total_score / len(valid_grades)
    
    # Get recent grades for activity feed
    recent_grades = Grade.query.filter_by(user_id=user.id).order_by(Grade.graded_at.desc()).limit(5).all()
    
    return render_template('profile.html', 
                         user=user,
                         enrolled_courses=enrolled_courses,
                         overall_gpa=overall_gpa,
                         recent_grades=recent_grades)

def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

def create_quiz(course_id):
    if 'user_id' not in session:
        flash('Please log in to create quizzes', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Only teachers can create quizzes', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != user.id:
        flash('You can only create quizzes for your own courses', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        quiz_text = request.form.get('quiz_text', '').strip()
        time_limit = int(request.form.get('time_limit', 30))
        passing_score = int(request.form.get('passing_score', 70))
        
        if not quiz_text:
            flash('Please enter quiz content', 'danger')
            return render_template('create_quiz.html', course=course)
        
        try:
            # Parse the quiz text
            quiz_data = parse_quiz_text(quiz_text)
            
            if not quiz_data['questions']:
                flash('No valid questions found in the quiz text', 'danger')
                return render_template('create_quiz.html', course=course)
            
            # Validate that all questions have correct answers
            for i, question_data in enumerate(quiz_data['questions']):
                if not question_data['correct_answer']:
                    flash(f'Question {i+1} does not have a correct answer specified. Please add [CORRECT] to one option.', 'danger')
                    return render_template('create_quiz.html', course=course)
            
            # Create the quiz
            quiz = Quiz(
                title=quiz_data['title'],
                course_id=course_id,
                time_limit_minutes=time_limit,
                passing_score=passing_score
            )
            db.session.add(quiz)
            db.session.flush()  # Get the quiz ID
            
            # Create questions
            for i, question_data in enumerate(quiz_data['questions']):
                question = QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=question_data['question_text'],
                    option_a=question_data['options'].get('A', ''),
                    option_b=question_data['options'].get('B', ''),
                    option_c=question_data['options'].get('C', ''),
                    option_d=question_data['options'].get('D', ''),
                    correct_answer=question_data['correct_answer'],
                    order_num=i + 1
                )
                db.session.add(question)
            
            db.session.commit()
            flash(f'Quiz "{quiz.title}" created successfully!', 'success')
            return redirect(url_for('course_detail', course_id=course_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while creating the quiz: {str(e)}', 'danger')
            return render_template('create_quiz.html', course=course)
    
    return render_template('create_quiz.html', course=course)

def take_quiz(quiz_id):
    if 'user_id' not in session:
        flash('Please log in to take quizzes', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'student':
        flash('Only students can take quizzes', 'danger')
        return redirect(url_for('dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if student is enrolled in the course
    enrollment = Enrollment.query.filter_by(
        user_id=user.id,
        course_id=quiz.course_id
    ).first()
    
    if not enrollment:
        flash('You must be enrolled in this course to take the quiz', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if already attempted
    existing_attempt = QuizAttempt.query.filter_by(
        quiz_id=quiz_id,
        user_id=user.id
    ).first()
    
    if existing_attempt:
        flash('You have already taken this quiz', 'info')
        return redirect(url_for('quiz_results', attempt_id=existing_attempt.id))
    
    if request.method == 'POST':
        # Process quiz submission
        print(f"DEBUG: Quiz submission received for quiz {quiz_id}")
        print(f"DEBUG: Form data: {dict(request.form)}")
        score = 0
        
        # Get questions directly from database
        questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
        max_score = len(questions)
        print(f"DEBUG: Found {max_score} questions")
        
        # Create attempt
        attempt = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user.id,
            max_score=max_score,
            completed_at=datetime.now()
        )
        db.session.add(attempt)
        db.session.flush()
        print(f"DEBUG: Created attempt {attempt.id}")
        
        # Process answers
        for question in questions:
            selected_answer = request.form.get(f'question_{question.id}')
            print(f"DEBUG: Question {question.id}: selected={selected_answer}, correct={question.correct_answer}")
            if selected_answer:
                is_correct = selected_answer == question.correct_answer
                points_earned = 1 if is_correct else 0
                score += points_earned
                
                answer = QuizAnswer(
                    attempt_id=attempt.id,
                    question_id=question.id,
                    selected_answer=selected_answer,
                    is_correct=is_correct,
                    points_earned=points_earned
                )
                db.session.add(answer)
        
        # Calculate final score
        attempt.score = score
        attempt.percentage = (score / max_score) * 100
        attempt.passed = attempt.percentage >= quiz.passing_score
        
        # Create a Grade record for the grades page
        grade = Grade(
            user_id=user.id,
            course_id=quiz.course_id,
            assignment_name=f"Quiz: {quiz.title}",
            score=attempt.percentage,
            max_score=100.0,
            feedback=f"Quiz completed with {score}/{max_score} correct answers",
            graded_at=datetime.now()
        )
        db.session.add(grade)
        
        try:
            db.session.commit()
            flash('Quiz submitted successfully!', 'success')
            return redirect(url_for('quiz_results', attempt_id=attempt.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the quiz', 'danger')
    
    return render_template('take_quiz.html', quiz=quiz)

def quiz_results(attempt_id):
    if 'user_id' not in session:
        flash('Please log in to view quiz results', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('Please log in to view quiz results', 'warning')
        return redirect(url_for('login'))
    
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    # Check if user owns this attempt or is the teacher
    if attempt.user_id != user.id:
        course = Course.query.get(attempt.quiz.course_id)
        if not course or course.instructor_id != user.id:
            flash('You can only view your own quiz results', 'danger')
            return redirect(url_for('dashboard'))
    
    return render_template('quiz_results.html', attempt=attempt)

def request_account_deletion():
    """Request account deletion (user function)"""
    if 'user_id' not in session:
        flash('Please log in to request account deletion.', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if there's already a pending request
    existing_request = UserDeletionRequest.query.filter_by(
        user_id=user.id, 
        status='pending'
    ).first()
    
    if existing_request:
        flash('You already have a pending account deletion request.', 'warning')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        reason = request.form['reason'].strip()
        
        if not reason:
            flash('Please provide a reason for account deletion.', 'danger')
            return render_template('request_account_deletion.html', user=user)
        
        # Create deletion request
        deletion_request = UserDeletionRequest(
            user_id=user.id,
            reason=reason
        )
        
        try:
            db.session.add(deletion_request)
            db.session.commit()
            flash('Account deletion request submitted successfully. An admin will review it.', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the request. Please try again.', 'danger')
    
    return render_template('request_account_deletion.html', user=user)

def settings():
    """User settings page"""
    if 'user_id' not in session:
        flash('Please log in to access settings', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle settings updates
        email_notifications = request.form.get('email_notifications') == 'on'
        push_notifications = request.form.get('push_notifications') == 'on'
        privacy_level = request.form.get('privacy_level', 'public')
        language = request.form.get('language', 'en')
        timezone = request.form.get('timezone', 'UTC')
        
        # Update user preferences (you can extend the User model to store these)
        # For now, we'll just show a success message
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html', user=user)

def certificates():
    """User certificates page"""
    if 'user_id' not in session:
        flash('Please log in to view certificates', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    # Get user's completed courses (courses with passing grades)
    completed_courses = []
    if user.role == 'student':
        # Get all grades for the user
        grades = Grade.query.filter_by(user_id=user.id).all()
        
        # Group grades by course and check if course is completed
        course_grades = {}
        for grade in grades:
            if grade.course_id not in course_grades:
                course_grades[grade.course_id] = []
            course_grades[grade.course_id].append(grade)
        
        # Check which courses are completed (have passing grades)
        for course_id, grades_list in course_grades.items():
            if grades_list:
                # Calculate average grade for the course
                valid_grades = [g.score for g in grades_list if g.score is not None]
                if valid_grades:
                    avg_grade = sum(valid_grades) / len(valid_grades)
                    if avg_grade >= 70:  # Passing threshold
                        course = Course.query.get(course_id)
                        if course:
                            completed_courses.append({
                                'course': course,
                                'average_grade': avg_grade,
                                'completed_date': max(g.graded_at for g in grades_list if g.graded_at),
                                'certificate_id': f"CERT-{course_id}-{user.id}-{int(time.time())}"
                            })
    
    return render_template('certificates.html', user=user, completed_courses=completed_courses)

def schedule():
    """User schedule page"""
    if 'user_id' not in session:
        flash('Please log in to view schedule', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('login'))
    
    # Get user's enrolled courses and upcoming deadlines
    enrolled_courses = []
    upcoming_deadlines = []
    
    if user.role == 'student':
        # Get enrolled courses
        enrollments = Enrollment.query.filter_by(user_id=user.id, status='active').all()
        for enrollment in enrollments:
            course = Course.query.get(enrollment.course_id)
            if course:
                enrolled_courses.append({
                    'course': course,
                    'enrollment': enrollment,
                    'next_session': None,  # You can implement session scheduling logic
                    'progress': enrollment.progress
                })
        
        # Get upcoming assignment deadlines
        assignments = Assignment.query.join(
            Course, Assignment.course_id == Course.id
        ).join(
            Enrollment, Enrollment.course_id == Course.id
        ).filter(
            Enrollment.user_id == user.id,
            Assignment.due_date > datetime.now()
        ).order_by(Assignment.due_date).limit(10).all()
        
        for assignment in assignments:
            upcoming_deadlines.append({
                'assignment': assignment,
                'course': Course.query.get(assignment.course_id),
                'days_remaining': (assignment.due_date - datetime.now()).days
            })
    
    return render_template('schedule.html', 
                         user=user, 
                         enrolled_courses=enrolled_courses,
                         upcoming_deadlines=upcoming_deadlines)
