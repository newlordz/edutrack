from flask import render_template, request, redirect, url_for, flash, session
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement
from database import db

def admin_dashboard():
    """Admin dashboard showing system overview"""
    if 'user_id' not in session:
        flash('Please log in to access admin dashboard', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get system statistics
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    total_grades = Grade.query.count()
    
    # Get users by role
    students = User.query.filter_by(role='student').count()
    teachers = User.query.filter_by(role='teacher').count()
    admins = User.query.filter_by(role='admin').count()
    
    # Get recent activities
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         user=user,
                         total_users=total_users,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         total_grades=total_grades,
                         students=students,
                         teachers=teachers,
                         admins=admins,
                         recent_users=recent_users,
                         recent_courses=recent_courses)

def manage_users():
    """Manage all users in the system"""
    if 'user_id' not in session:
        flash('Please log in to manage users', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all users with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    users_pagination = User.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/manage_users.html', 
                         user=user,
                         users=users_pagination.items,
                         pagination=users_pagination)

def edit_user(user_id):
    """Edit user information"""
    if 'user_id' not in session:
        flash('Please log in to edit users', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    target_user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        target_user.first_name = request.form['first_name']
        target_user.last_name = request.form['last_name']
        target_user.email = request.form['email']
        target_user.role = request.form['role']
        
        db.session.commit()
        flash(f'User {target_user.username} updated successfully!', 'success')
        return redirect(url_for('manage_users'))
    
    return render_template('admin/edit_user.html', 
                         user=admin_user,
                         target_user=target_user)

def delete_user(user_id):
    """Delete a user"""
    if 'user_id' not in session:
        flash('Please log in to delete users', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    target_user = User.query.get_or_404(user_id)
    
    if target_user.id == admin_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('manage_users'))
    
    username = target_user.username
    db.session.delete(target_user)
    db.session.commit()
    
    flash(f'User {username} deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

def manage_courses():
    """Manage all courses in the system"""
    if 'user_id' not in session:
        flash('Please log in to manage courses', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all courses with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 15
    courses_pagination = Course.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/manage_courses.html', 
                         user=user,
                         courses=courses_pagination.items,
                         pagination=courses_pagination)

def edit_course(course_id):
    """Edit course information"""
    if 'user_id' not in session:
        flash('Please log in to edit courses', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    teachers = User.query.filter_by(role='teacher').all()
    
    if request.method == 'POST':
        course.title = request.form['title']
        course.description = request.form['description']
        course.duration_weeks = int(request.form['duration_weeks'])
        course.difficulty = request.form['difficulty']
        course.max_students = int(request.form['max_students'])
        
        # Update instructor if changed
        instructor_id = request.form.get('instructor_id')
        if instructor_id:
            instructor = User.query.get(instructor_id)
            if instructor and instructor.role == 'teacher':
                course.instructor = instructor.first_name + " " + instructor.last_name
                course.instructor_id = instructor.id
        
        db.session.commit()
        flash(f'Course "{course.title}" updated successfully!', 'success')
        return redirect(url_for('manage_courses'))
    
    return render_template('admin/edit_course.html', 
                         user=admin_user,
                         course=course,
                         teachers=teachers)

def delete_course(course_id):
    """Delete a course"""
    if 'user_id' not in session:
        flash('Please log in to delete courses', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    course = Course.query.get_or_404(course_id)
    title = course.title
    
    db.session.delete(course)
    db.session.commit()
    
    flash(f'Course "{title}" deleted successfully!', 'success')
    return redirect(url_for('manage_courses'))

def system_analytics():
    """View system analytics and reports"""
    if 'user_id' not in session:
        flash('Please log in to view analytics', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get analytics data
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    
    # Course popularity
    course_enrollments = []
    for course in Course.query.all():
        course_enrollments.append({
            'course': course,
            'enrollment_count': len(course.enrollments),
            'completion_rate': len([e for e in course.enrollments if e.status == 'completed']) / len(course.enrollments) * 100 if course.enrollments else 0
        })
    
    course_enrollments.sort(key=lambda x: x['enrollment_count'], reverse=True)
    
    # User activity
    active_users = User.query.filter(User.enrollments.any()).count()
    inactive_users = total_users - active_users
    
    return render_template('admin/analytics.html', 
                         user=user,
                         total_users=total_users,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         course_enrollments=course_enrollments[:10],  # Top 10
                         active_users=active_users,
                         inactive_users=inactive_users) 