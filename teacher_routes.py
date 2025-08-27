from flask import render_template, request, redirect, url_for, flash, session, current_app
from database import db
from models import User, Course, CourseMaterial, Announcement, Assignment, AssignmentSubmission, StudyProgress, Grade, Enrollment, CourseDeletionRequest, Quiz, QuizQuestion, QuizAttempt, QuizAnswer
from datetime import datetime
import os

def teacher_dashboard():
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    teacher_id = session['user_id']
    teacher_courses = Course.query.filter_by(instructor_id=teacher_id).all()
    
    # Get recent assignments and submissions
    recent_assignments = Assignment.query.filter_by(created_by=teacher_id).order_by(Assignment.created_at.desc()).limit(5).all()
    pending_submissions = AssignmentSubmission.query.join(
        Assignment, 
        AssignmentSubmission.assignment_id == Assignment.id
    ).filter(
        Assignment.created_by == teacher_id,
        AssignmentSubmission.status == 'submitted'
    ).count()
    
    # Get teacher user object
    teacher = User.query.get(teacher_id)
    
    # Calculate total students across all courses
    total_students = sum(len(course.enrollments) for course in teacher_courses)
    
    # Get recent grades for the teacher's courses
    recent_grades = []
    for course in teacher_courses:
        grades = Grade.query.filter_by(course_id=course.id).order_by(Grade.graded_at.desc()).limit(3).all()
        recent_grades.extend(grades)
    
    # Sort by graded date and limit to 5 most recent
    recent_grades = sorted(recent_grades, key=lambda x: x.graded_at, reverse=True)[:5]
    
    return render_template('teacher/dashboard.html', 
                         user=teacher,
                         teacher_courses=teacher_courses,
                         total_students=total_students,
                         recent_grades=recent_grades,
                         recent_assignments=recent_assignments,
                         pending_submissions=pending_submissions)

def create_course():
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        duration_weeks = int(request.form['duration_weeks'])
        difficulty = request.form['difficulty']
        max_students = int(request.form['max_students'])
        
        if not all([title, description, duration_weeks, difficulty, max_students]):
            flash('All fields are required', 'danger')
            return render_template('teacher/create_course.html')
        
        course = Course(
            title=title,
            description=description,
            instructor_id=session['user_id'],
            instructor=session['username'],
            duration_weeks=duration_weeks,
            difficulty=difficulty,
            max_students=max_students
        )
        
        try:
            db.session.add(course)
            db.session.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('teacher_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the course.', 'danger')
    
    return render_template('teacher/create_course.html')

def manage_course(course_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get course statistics and enrolled students data
    enrollments = course.enrollments
    assignments = Assignment.query.filter_by(course_id=course_id).all()
    materials = CourseMaterial.query.filter_by(course_id=course_id).order_by(CourseMaterial.order_index).all()
    
    # Prepare enrolled students data with grades for the template
    enrolled_students_data = []
    for enrollment in enrollments:
        student = enrollment.student
        # Get grades for this student in this course
        grades = Grade.query.filter_by(user_id=student.id, course_id=course_id).all()
        enrolled_students_data.append({
            'student': student,
            'enrollment': enrollment,
            'grades': grades
        })
    
    return render_template('teacher/manage_course.html',
                         course=course,
                         enrolled_students=enrolled_students_data,
                         assignments=assignments,
                         materials=materials)

def upload_material(course_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only upload materials to your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        order_index = int(request.form.get('order_index', 0))
        
        if not title:
            flash('Title is required', 'danger')
            return render_template('teacher/upload_material.html', course=course)
        
        # Handle file upload
        file_path = None
        file_type = None
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename:
                # Create uploads directory if it doesn't exist
                upload_dir = os.path.join(current_app.root_path, 'uploads')
                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)
                
                # Generate unique filename
                filename = f"{course_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
                file_path = os.path.join(upload_dir, filename)
                file_type = file.filename.split('.')[-1].lower() if '.' in file.filename else 'unknown'
                
                # Save the file
                try:
                    file.save(file_path)
                    # Store relative path for database
                    file_path = f"uploads/{filename}"
                    
                    # Debug: Print file information
                    print(f"DEBUG: File saved successfully")
                    print(f"DEBUG: Full file path: {file_path}")
                    print(f"DEBUG: File type: {file_type}")
                    print(f"DEBUG: File exists: {os.path.exists(file_path)}")
                    
                except Exception as e:
                    flash(f'Error saving file: {str(e)}', 'danger')
                    return render_template('teacher/upload_material.html', course=course)
        
        material = CourseMaterial(
            course_id=course_id,
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_type,
            uploaded_by=session['user_id'],
            order_index=order_index
        )
        
        try:
            db.session.add(material)
            db.session.commit()
            flash('Material uploaded successfully!', 'success')
            return redirect(url_for('manage_course', course_id=course_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while uploading the material.', 'danger')
    
    return render_template('teacher/upload_material.html', course=course)

def create_assignment(course_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only create assignments for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        due_date_str = request.form['due_date']
        max_score = float(request.form['max_score'])
        assignment_type = request.form['assignment_type']
        instructions = request.form['instructions'].strip()
        
        if not all([title, description, due_date_str, max_score]):
            flash('Title, description, due date, and max score are required', 'danger')
            return render_template('teacher/create_assignment.html', course=course)
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid due date format', 'danger')
            return render_template('teacher/create_assignment.html', course=course)
        
        assignment = Assignment(
            course_id=course_id,
            title=title,
            description=description,
            due_date=due_date,
            max_score=max_score,
            assignment_type=assignment_type,
            instructions=instructions,
            created_by=session['user_id']
        )
        
        try:
            db.session.add(assignment)
            db.session.commit()
            flash('Assignment created successfully!', 'success')
            return redirect(url_for('manage_course', course_id=course_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the assignment.', 'danger')
    
    return render_template('teacher/create_assignment.html', course=course)

def grade_assignment(submission_id=None, course_id=None, student_id=None):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    # Handle both submission_id and course_id/student_id cases
    if submission_id:
        submission = AssignmentSubmission.query.get_or_404(submission_id)
        assignment = submission.assignment
        course = assignment.course
    elif course_id and student_id:
        # Find the most recent submission for this student in this course
        submission = AssignmentSubmission.query.join(
            Assignment, 
            AssignmentSubmission.assignment_id == Assignment.id
        ).filter(
            AssignmentSubmission.user_id == student_id,
            Assignment.course_id == course_id
        ).order_by(AssignmentSubmission.submitted_at.desc()).first()
        
        if not submission:
            flash('No submissions found for this student in this course.', 'warning')
            return redirect(url_for('manage_course', course_id=course_id))
        
        assignment = submission.assignment
        course = assignment.course
    else:
        flash('Invalid parameters for grading.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only grade assignments from your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        score = float(request.form['score'])
        feedback = request.form['feedback'].strip()
        
        if score < 0 or score > assignment.max_score:
            flash('Score must be between 0 and the maximum score', 'danger')
            return render_template('teacher/grade_assignment.html', submission=submission)
        
        submission.score = score
        submission.feedback = feedback
        submission.graded_by = session['user_id']
        submission.graded_at = datetime.utcnow()
        submission.status = 'graded'
        
        # Update student's grade record
        grade = Grade.query.filter_by(
            user_id=submission.user_id,
            course_id=course.id,
            assignment_name=assignment.title
        ).first()
        
        if not grade:
            grade = Grade(
                user_id=submission.user_id,
                course_id=course.id,
                assignment_name=assignment.title,
                score=score,
                max_score=assignment.max_score,
                feedback=feedback
            )
            db.session.add(grade)
        else:
            grade.score = score
            grade.feedback = feedback
        
        try:
            db.session.commit()
            flash('Assignment graded successfully!', 'success')
            return redirect(url_for('manage_course', course_id=course.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while grading the assignment.', 'danger')
    
    return render_template('teacher/grade_assignment.html', submission=submission)

def view_submissions(assignment_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only view submissions from your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    submissions = AssignmentSubmission.query.filter_by(assignment_id=assignment_id).all()
    
    return render_template('teacher/view_submissions.html',
                         assignment=assignment,
                         submissions=submissions)

def create_announcement(course_id):
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only create announcements for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        
        if not all([title, content]):
            flash('Title and content are required', 'danger')
            return render_template('teacher/create_announcement.html', course=course)
        
        announcement = Announcement(
            course_id=course_id,
            title=title,
            content=content,
            created_by=session['user_id']
        )
        
        try:
            db.session.add(announcement)
            db.session.commit()
            flash('Announcement created successfully!', 'success')
            return redirect(url_for('manage_course', course_id=course_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the announcement.', 'danger')
    
    return render_template('teacher/create_announcement.html', course=course)

def unenroll_student(course_id, student_id):
    """Unenroll a student from a course (only by the teacher who created it)"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    student = User.query.get_or_404(student_id)
    enrollment = Enrollment.query.filter_by(
        user_id=student_id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        flash('Student is not enrolled in this course.', 'danger')
        return redirect(url_for('manage_course', course_id=course_id))
    
    try:
        # Delete related data first
        # Delete study progress
        StudyProgress.query.filter_by(
            user_id=student_id,
            course_id=course_id
        ).delete()
        
        # Delete assignment submissions
        assignments = Assignment.query.filter_by(course_id=course_id).all()
        for assignment in assignments:
            AssignmentSubmission.query.filter_by(
                assignment_id=assignment.id,
                user_id=student_id
            ).delete()
        
        # Delete grades
        Grade.query.filter_by(
            user_id=student_id,
            course_id=course_id
        ).delete()
        
        # Delete enrollment
        db.session.delete(enrollment)
        db.session.commit()
        
        flash(f'Student {student.first_name} {student.last_name} has been unenrolled from {course.title}.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while unenrolling the student. Please try again.', 'danger')
    
    return redirect(url_for('manage_course', course_id=course_id))

def unenroll_all_students(course_id):
    """Unenroll all students from a course (only by the teacher who created it)"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        try:
            # Get all enrollments
            enrollments = Enrollment.query.filter_by(course_id=course_id).all()
            student_count = len(enrollments)
            
            if student_count == 0:
                flash('No students are enrolled in this course.', 'info')
                return redirect(url_for('manage_course', course_id=course_id))
            
            # Delete related data for all students
            for enrollment in enrollments:
                student_id = enrollment.user_id
                
                # Delete study progress
                StudyProgress.query.filter_by(
                    user_id=student_id,
                    course_id=course_id
                ).delete()
                
                # Delete assignment submissions
                assignments = Assignment.query.filter_by(course_id=course_id).all()
                for assignment in assignments:
                    AssignmentSubmission.query.filter_by(
                        assignment_id=assignment.id,
                        user_id=student_id
                    ).delete()
                
                # Delete grades
                Grade.query.filter_by(
                    user_id=student_id,
                    course_id=course_id
                ).delete()
                
                # Delete enrollment
                db.session.delete(enrollment)
            
            db.session.commit()
            flash(f'Successfully unenrolled {student_count} student(s) from {course.title}.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while unenrolling students. Please try again.', 'danger')
    
    return redirect(url_for('manage_course', course_id=course_id))

def request_course_deletion(course_id):
    """Request course deletion (teacher function)"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only request deletion for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Check if there's already a pending request
    existing_request = CourseDeletionRequest.query.filter_by(
        course_id=course_id, 
        status='pending'
    ).first()
    
    if existing_request:
        flash('You already have a pending deletion request for this course.', 'warning')
        return redirect(url_for('manage_course', course_id=course_id))
    
    if request.method == 'POST':
        reason = request.form['reason'].strip()
        
        if not reason:
            flash('Please provide a reason for deletion.', 'danger')
            return render_template('teacher/request_course_deletion.html', course=course)
        
        # Create deletion request
        deletion_request = CourseDeletionRequest(
            course_id=course_id,
            requested_by=session['user_id'],
            reason=reason
        )
        
        try:
            db.session.add(deletion_request)
            db.session.commit()
            flash('Course deletion request submitted successfully. An admin will review it.', 'success')
            return redirect(url_for('manage_course', course_id=course_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the request. Please try again.', 'danger')
    
    return render_template('teacher/request_course_deletion.html', course=course)

def delete_course(course_id):
    """Delete a course (only by the teacher who created it)"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only delete your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        # Check if there are enrolled students
        if len(course.enrollments) > 0:
            flash('Cannot delete course with enrolled students. Please unenroll all students first.', 'danger')
            return redirect(url_for('manage_course', course_id=course_id))
        
        course_title = course.title
        
        try:
            # Delete related data first (cascade delete would be better, but this is safer)
            # Delete assignments and submissions
            assignments = Assignment.query.filter_by(course_id=course_id).all()
            for assignment in assignments:
                AssignmentSubmission.query.filter_by(assignment_id=assignment.id).delete()
            Assignment.query.filter_by(course_id=course_id).delete()
            
            # Delete course materials
            CourseMaterial.query.filter_by(course_id=course_id).delete()
            
            # Delete announcements
            Announcement.query.filter_by(course_id=course_id).delete()
            
            # Delete study progress
            StudyProgress.query.filter_by(course_id=course_id).delete()
            
            # Delete the course itself
            db.session.delete(course)
            db.session.commit()
            
            flash(f'Course "{course_title}" has been deleted successfully.', 'success')
            return redirect(url_for('teacher_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the course. Please try again.', 'danger')
            return redirect(url_for('manage_course', course_id=course_id))
    
    # Show confirmation page
    return render_template('teacher/delete_course.html', course=course)

# ==================== QUIZ MANAGEMENT FUNCTIONS ====================

def manage_quizzes(course_id):
    """View and manage all quizzes for a course"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage quizzes for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get all quizzes for this course with attempt statistics
    quizzes = Quiz.query.filter_by(course_id=course_id).order_by(Quiz.created_at.desc()).all()
    
    quiz_stats = []
    for quiz in quizzes:
        attempts = QuizAttempt.query.filter_by(quiz_id=quiz.id).all()
        total_attempts = len(attempts)
        passed_attempts = len([a for a in attempts if a.passed])
        avg_score = sum([a.percentage for a in attempts]) / total_attempts if total_attempts > 0 else 0
        
        quiz_stats.append({
            'quiz': quiz,
            'total_attempts': total_attempts,
            'passed_attempts': passed_attempts,
            'avg_score': round(avg_score, 1)
        })
    
    return render_template('teacher/manage_quizzes.html', 
                         course=course, 
                         quiz_stats=quiz_stats)

def quiz_results_overview(quiz_id):
    """View all student results for a specific quiz"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    course = Course.query.get_or_404(quiz.course_id)
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only view results for quizzes in your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get all attempts for this quiz with student details
    attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).order_by(QuizAttempt.completed_at.desc()).all()
    
    # Calculate quiz statistics
    total_attempts = len(attempts)
    passed_attempts = len([a for a in attempts if a.passed])
    avg_score = sum([a.percentage for a in attempts]) / total_attempts if total_attempts > 0 else 0
    highest_score = max([a.percentage for a in attempts]) if attempts else 0
    lowest_score = min([a.percentage for a in attempts]) if attempts else 0
    
    return render_template('teacher/quiz_results_overview.html',
                         quiz=quiz,
                         course=course,
                         attempts=attempts,
                         total_attempts=total_attempts,
                         passed_attempts=passed_attempts,
                         avg_score=round(avg_score, 1),
                         highest_score=round(highest_score, 1),
                         lowest_score=round(lowest_score, 1))

def edit_quiz_answers(quiz_id):
    """Edit correct answers and scoring for a quiz"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    course = Course.query.get_or_404(quiz.course_id)
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only edit quizzes in your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        try:
            # Update correct answers and points for each question
            for question in quiz.questions:
                question_id = str(question.id)
                correct_answer = request.form.get(f'correct_answer_{question_id}')
                points = int(request.form.get(f'points_{question_id}', 1))
                
                if correct_answer in ['A', 'B', 'C', 'D']:
                    question.correct_answer = correct_answer
                    question.points = points
            
            # Recalculate all existing attempts with new answers
            attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).all()
            for attempt in attempts:
                total_score = 0
                max_score = 0
                
                for answer in attempt.answers:
                    question = answer.question
                    max_score += question.points
                    
                    if answer.selected_answer == question.correct_answer:
                        answer.is_correct = True
                        answer.points_earned = question.points
                        total_score += question.points
                    else:
                        answer.is_correct = False
                        answer.points_earned = 0
                
                # Update attempt scores
                attempt.score = total_score
                attempt.max_score = max_score
                attempt.percentage = (total_score / max_score * 100) if max_score > 0 else 0
                attempt.passed = attempt.percentage >= quiz.passing_score
            
            db.session.commit()
            flash('Quiz answers updated successfully! All existing attempts have been re-graded.', 'success')
            return redirect(url_for('quiz_results_overview', quiz_id=quiz_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating quiz answers: {str(e)}', 'danger')
    
    return render_template('teacher/edit_quiz_answers.html', quiz=quiz, course=course)

def delete_quiz(quiz_id):
    """Delete a quiz and all its attempts"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    course = Course.query.get_or_404(quiz.course_id)
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only delete quizzes in your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        quiz_title = quiz.title
        try:
            db.session.delete(quiz)
            db.session.commit()
            flash(f'Quiz "{quiz_title}" has been deleted successfully.', 'success')
            return redirect(url_for('manage_quizzes', course_id=course.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the quiz. Please try again.', 'danger')
    
    return render_template('teacher/delete_quiz.html', quiz=quiz, course=course) 

def manage_assignments(course_id):
    """Manage all assignments for a course"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage assignments for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get all assignments for this course
    assignments = Assignment.query.filter_by(course_id=course_id).order_by(Assignment.due_date.desc()).all()
    
    # Get submission counts for each assignment
    for assignment in assignments:
        assignment.submission_count = AssignmentSubmission.query.filter_by(assignment_id=assignment.id).count()
        assignment.graded_count = AssignmentSubmission.query.filter_by(assignment_id=assignment.id, status='graded').count()
        assignment.pending_count = AssignmentSubmission.query.filter_by(assignment_id=assignment.id, status='submitted').count()
        assignment.late_count = AssignmentSubmission.query.filter_by(assignment_id=assignment.id, status='late').count()
    
    return render_template('teacher/manage_assignments.html', course=course, assignments=assignments)

def edit_assignment(assignment_id):
    """Edit an existing assignment"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only edit assignments for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        due_date_str = request.form['due_date']
        max_score = float(request.form['max_score'])
        assignment_type = request.form['assignment_type']
        instructions = request.form['instructions'].strip()
        is_active = 'is_active' in request.form
        
        if not all([title, description, due_date_str, max_score]):
            flash('Title, description, due date, and max score are required', 'danger')
            return render_template('teacher/edit_assignment.html', assignment=assignment, course=course)
        
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid due date format', 'danger')
            return render_template('teacher/edit_assignment.html', assignment=assignment, course=course)
        
        # Update assignment
        assignment.title = title
        assignment.description = description
        assignment.due_date = due_date
        assignment.max_score = max_score
        assignment.assignment_type = assignment_type
        assignment.instructions = instructions
        assignment.is_active = is_active
        
        try:
            db.session.commit()
            flash('Assignment updated successfully!', 'success')
            return redirect(url_for('manage_assignments', course_id=course.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the assignment.', 'danger')
    
    return render_template('teacher/edit_assignment.html', assignment=assignment, course=course)

def delete_assignment(assignment_id):
    """Delete an assignment and all its submissions"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only delete assignments for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        try:
            # Delete all submissions first
            AssignmentSubmission.query.filter_by(assignment_id=assignment_id).delete()
            
            # Delete the assignment
            db.session.delete(assignment)
            db.session.commit()
            
            flash(f'Assignment "{assignment.title}" deleted successfully!', 'success')
            return redirect(url_for('manage_assignments', course_id=course.id))
            
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the assignment.', 'danger')
    
    return render_template('teacher/delete_assignment.html', assignment=assignment, course=course)

def toggle_assignment_status(assignment_id):
    """Toggle assignment active/inactive status"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only manage assignments for your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    try:
        assignment.is_active = not assignment.is_active
        status = "activated" if assignment.is_active else "deactivated"
        db.session.commit()
        flash(f'Assignment "{assignment.title}" {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the assignment status.', 'danger')
    
    return redirect(url_for('manage_assignments', course_id=course.id))

def assignment_analytics(assignment_id):
    """View detailed analytics for an assignment"""
    if 'user_id' not in session or session.get('role') != 'teacher':
        flash('Access denied. Teacher login required.', 'danger')
        return redirect(url_for('login'))
    
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course
    
    if course.instructor_id != session['user_id']:
        flash('Access denied. You can only view analytics for your own assignments.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get all submissions
    submissions = AssignmentSubmission.query.filter_by(assignment_id=assignment_id).all()
    
    # Calculate statistics
    total_submissions = len(submissions)
    graded_submissions = len([s for s in submissions if s.status == 'graded'])
    pending_submissions = len([s for s in submissions if s.status == 'submitted'])
    late_submissions = len([s for s in submissions if s.status == 'late'])
    
    # Calculate average score
    graded_scores = [s.score for s in submissions if s.score is not None]
    average_score = sum(graded_scores) / len(graded_scores) if graded_scores else 0
    
    # Get submission distribution by date
    submission_dates = {}
    for submission in submissions:
        date_str = submission.submitted_at.strftime('%Y-%m-%d')
        submission_dates[date_str] = submission_dates.get(date_str, 0) + 1
    
    return render_template('teacher/assignment_analytics.html', 
                         assignment=assignment, 
                         course=course,
                         submissions=submissions,
                         total_submissions=total_submissions,
                         graded_submissions=graded_submissions,
                         pending_submissions=pending_submissions,
                         late_submissions=late_submissions,
                         average_score=average_score,
                         submission_dates=submission_dates) 