from flask import render_template, request, redirect, url_for, flash, session
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement
from database import db
import os
from werkzeug.utils import secure_filename

def teacher_dashboard():
    """Teacher dashboard showing their courses and students"""
    if 'user_id' not in session:
        flash('Please log in to access your dashboard', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get courses taught by this teacher
    teacher_courses = Course.query.filter_by(instructor_id=user.id).all()
    
    # Get total students across all courses
    total_students = sum(len(course.enrollments) for course in teacher_courses)
    
    # Get recent grades for teacher's courses
    recent_grades = []
    for course in teacher_courses:
        course_grades = Grade.query.filter_by(course_id=course.id).order_by(Grade.graded_at.desc()).limit(3).all()
        recent_grades.extend(course_grades)
    
    recent_grades = sorted(recent_grades, key=lambda x: x.graded_at, reverse=True)[:5]
    
    return render_template('teacher/dashboard.html', 
                         user=user,
                         teacher_courses=teacher_courses,
                         total_students=total_students,
                         recent_grades=recent_grades)

def create_course():
    """Create a new course"""
    if 'user_id' not in session:
        flash('Please log in to create courses', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        duration_weeks = int(request.form['duration_weeks'])
        difficulty = request.form['difficulty']
        max_students = int(request.form['max_students'])
        
        course = Course(
            title=title,
            description=description,
            instructor=user.first_name + " " + user.last_name,
            instructor_id=user.id,
            duration_weeks=duration_weeks,
            difficulty=difficulty,
            max_students=max_students
        )
        
        db.session.add(course)
        db.session.commit()
        
        flash(f'Course "{title}" created successfully!', 'success')
        return redirect(url_for('teacher_dashboard'))
    
    return render_template('teacher/create_course.html', user=user)

def manage_course(course_id):
    """Manage a specific course"""
    if 'user_id' not in session:
        flash('Please log in to manage courses', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != user.id:
        flash('Access denied. You can only manage your own courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    # Get enrolled students
    enrolled_students = []
    for enrollment in course.enrollments:
        student = User.query.get(enrollment.user_id)
        if student:
            enrolled_students.append({
                'student': student,
                'enrollment': enrollment,
                'grades': Grade.query.filter_by(user_id=student.id, course_id=course.id).all()
            })
    
    return render_template('teacher/manage_course.html', 
                         user=user,
                         course=course,
                         enrolled_students=enrolled_students)

def grade_assignment(course_id, student_id):
    """Grade a student's assignment"""
    if 'user_id' not in session:
        flash('Please log in to grade assignments', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != user.id:
        flash('Access denied. You can only grade assignments for your courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        assignment_name = request.form['assignment_name']
        score = float(request.form['score'])
        feedback = request.form['feedback']
        
        grade = Grade(
            user_id=student_id,
            course_id=course_id,
            assignment_name=assignment_name,
            score=score,
            feedback=feedback
        )
        
        db.session.add(grade)
        db.session.commit()
        
        flash(f'Grade for {assignment_name} submitted successfully!', 'success')
        return redirect(url_for('manage_course', course_id=course_id))
    
    student = User.query.get_or_404(student_id)
    return render_template('teacher/grade_assignment.html', 
                         user=user,
                         course=course,
                         student=student)

def upload_material(course_id):
    """Upload course material"""
    if 'user_id' not in session:
        flash('Please log in to upload materials', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != user.id:
        flash('Access denied. You can only upload materials for your courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        # Handle file upload (simplified - in production you'd want proper file handling)
        file_path = ""
        file_type = "document"
        
        material = CourseMaterial(
            course_id=course_id,
            title=title,
            description=description,
            file_path=file_path,
            file_type=file_type,
            uploaded_by=user.id
        )
        
        db.session.add(material)
        db.session.commit()
        
        flash(f'Material "{title}" uploaded successfully!', 'success')
        return redirect(url_for('manage_course', course_id=course_id))
    
    return render_template('teacher/upload_material.html', 
                         user=user,
                         course=course)

def create_announcement(course_id):
    """Create an announcement for a course"""
    if 'user_id' not in session:
        flash('Please log in to create announcements', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != user.id:
        flash('Access denied. You can only create announcements for your courses.', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        announcement = Announcement(
            course_id=course_id,
            title=title,
            content=content,
            created_by=user.id
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        flash(f'Announcement "{title}" created successfully!', 'success')
        return redirect(url_for('manage_course', course_id=course_id))
    
    return render_template('teacher/create_announcement.html', 
                         user=user,
                         course=course) 