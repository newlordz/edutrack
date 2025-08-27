from flask import render_template, request, redirect, url_for, flash, session
from models import User, Course, Enrollment, Grade, CourseMaterial, Announcement, CourseDeletionRequest, Assignment, AssignmentSubmission, StudyProgress, UserDeletionRequest, QuizAnswer, QuizAttempt
from database import db
from datetime import datetime

def admin_dashboard():
    """Admin dashboard with system overview"""
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
    
    # Get user counts by role
    students = User.query.filter_by(role='student').count()
    teachers = User.query.filter_by(role='teacher').count()
    admins = User.query.filter_by(role='admin').count()
    
    # Get pending deletion requests count
    pending_deletion_requests = CourseDeletionRequest.query.filter_by(status='pending').count()
    pending_user_deletion_requests = UserDeletionRequest.query.filter_by(status='pending').count()
    
    # Get recent courses
    recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         user=user,
                         total_users=total_users,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         students=students,
                         teachers=teachers,
                         admins=admins,
                         pending_deletion_requests=pending_deletion_requests,
                         pending_user_deletion_requests=pending_user_deletion_requests,
                         recent_courses=recent_courses,
                         recent_users=recent_users)

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

def create_course():
    """Create a new course (admin function)"""
    if 'user_id' not in session:
        flash('Please log in to create courses', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    teachers = User.query.filter_by(role='teacher').all()
    
    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        duration_weeks = int(request.form['duration_weeks'])
        difficulty = request.form['difficulty']
        max_students = int(request.form['max_students'])
        instructor_id = request.form.get('instructor_id')
        
        if not all([title, description, duration_weeks, difficulty, max_students]):
            flash('All fields are required', 'danger')
            return render_template('admin/create_course.html', teachers=teachers)
        
        # Get instructor name if assigned
        instructor_name = None
        if instructor_id:
            instructor = User.query.get(instructor_id)
            if instructor and instructor.role == 'teacher':
                instructor_name = f"{instructor.first_name} {instructor.last_name}"
        
        course = Course(
            title=title,
            description=description,
            instructor_id=instructor_id,
            instructor=instructor_name,
            duration_weeks=duration_weeks,
            difficulty=difficulty,
            max_students=max_students
        )
        
        try:
            db.session.add(course)
            db.session.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('manage_courses'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the course.', 'danger')
    
    return render_template('admin/create_course.html', teachers=teachers)

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
    
    # Calculate average completion rate
    total_completion_rate = 0
    courses_with_enrollments = 0
    for course_data in course_enrollments:
        if course_data['enrollment_count'] > 0:
            total_completion_rate += course_data['completion_rate']
            courses_with_enrollments += 1
    
    avg_completion_rate = total_completion_rate / courses_with_enrollments if courses_with_enrollments > 0 else 0
    
    # Get user roles distribution
    user_roles = {
        'student': User.query.filter_by(role='student').count(),
        'teacher': User.query.filter_by(role='teacher').count(),
        'admin': User.query.filter_by(role='admin').count()
    }
    
    # Get recent activities (placeholder for now)
    recent_activities = []
    
    return render_template('admin/analytics.html', 
                         user=user,
                         total_users=total_users,
                         total_courses=total_courses,
                         total_enrollments=total_enrollments,
                         avg_completion_rate=avg_completion_rate,
                         course_enrollments=course_enrollments[:10],  # Top 10
                         user_roles=user_roles,
                         recent_activities=recent_activities,
                         active_users=active_users,
                         inactive_users=inactive_users)

def manage_deletion_requests():
    """Manage course deletion requests from teachers"""
    if 'user_id' not in session:
        flash('Please log in to manage deletion requests', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all deletion requests with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    requests_pagination = CourseDeletionRequest.query.order_by(
        CourseDeletionRequest.created_at.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/manage_deletion_requests.html', 
                         user=user,
                         requests=requests_pagination.items,
                         pagination=requests_pagination)

def review_deletion_request(request_id):
    """Review and approve/deny a course deletion request"""
    if 'user_id' not in session:
        flash('Please log in to review deletion requests', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    deletion_request = CourseDeletionRequest.query.get_or_404(request_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        admin_notes = request.form.get('admin_notes', '').strip()
        
        if action == 'approve':
            # Check if course still has enrolled students
            if len(deletion_request.course.enrollments) > 0:
                flash('Cannot approve deletion for a course with enrolled students. Please unenroll all students first.', 'danger')
                return redirect(url_for('review_deletion_request', request_id=request_id))
            
            # Approve the deletion request
            deletion_request.status = 'approved'
            deletion_request.admin_notes = admin_notes
            deletion_request.reviewed_by = admin_user.id
            deletion_request.reviewed_at = datetime.utcnow()
            
            # Delete the course and related data
            course = deletion_request.course
            course_title = course.title
            
            try:
                # Delete related data first
                assignments = Assignment.query.filter_by(course_id=course.id).all()
                for assignment in assignments:
                    AssignmentSubmission.query.filter_by(assignment_id=assignment.id).delete()
                Assignment.query.filter_by(course_id=course.id).delete()
                
                CourseMaterial.query.filter_by(course_id=course.id).delete()
                Announcement.query.filter_by(course_id=course.id).delete()
                StudyProgress.query.filter_by(course_id=course.id).delete()
                
                # Delete the course itself
                db.session.delete(course)
                db.session.commit()
                
                flash(f'Course "{course_title}" deletion approved and course deleted successfully.', 'success')
                return redirect(url_for('manage_deletion_requests'))
                
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while deleting the course. Please try again.', 'danger')
                return redirect(url_for('review_deletion_request', request_id=request_id))
                
        elif action == 'deny':
            # Deny the deletion request
            deletion_request.status = 'denied'
            deletion_request.admin_notes = admin_notes
            deletion_request.reviewed_by = admin_user.id
            deletion_request.reviewed_at = datetime.utcnow()
            
            db.session.commit()
            flash('Course deletion request denied successfully.', 'success')
            return redirect(url_for('manage_deletion_requests'))
    
    return render_template('admin/review_deletion_request.html', 
                         user=admin_user,
                         deletion_request=deletion_request) 

def manage_user_deletion_requests():
    """Manage user account deletion requests"""
    if 'user_id' not in session:
        flash('Please log in to manage user deletion requests', 'warning')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user or user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get all user deletion requests with pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20
    requests_pagination = UserDeletionRequest.query.order_by(
        UserDeletionRequest.created_at.desc()
    ).paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return render_template('admin/manage_user_deletion_requests.html', 
                         user=user,
                         requests=requests_pagination.items,
                         pagination=requests_pagination)

def review_user_deletion_request(request_id):
    """Review and approve/deny a user account deletion request"""
    if 'user_id' not in session:
        flash('Please log in to review user deletion requests', 'warning')
        return redirect(url_for('login'))
    
    admin_user = User.query.get(session['user_id'])
    if not admin_user or admin_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard'))
    
    deletion_request = UserDeletionRequest.query.get_or_404(request_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        admin_notes = request.form.get('admin_notes', '').strip()
        
        if action == 'approve':
            # Approve the deletion request
            deletion_request.status = 'approved'
            deletion_request.admin_notes = admin_notes
            deletion_request.reviewed_by = admin_user.id
            deletion_request.reviewed_at = datetime.utcnow()
            
            # Delete the user and related data
            target_user = deletion_request.user
            username = target_user.username
            
            try:
                # Delete related data first
                # Delete grades
                Grade.query.filter_by(user_id=target_user.id).delete()
                
                # Delete study progress
                StudyProgress.query.filter_by(user_id=target_user.id).delete()
                
                # Delete assignment submissions
                AssignmentSubmission.query.filter_by(user_id=target_user.id).delete()
                
                # Delete quiz attempts and answers
                QuizAnswer.query.filter_by(user_id=target_user.id).delete()
                QuizAttempt.query.filter_by(user_id=target_user.id).delete()
                
                # Delete enrollments
                Enrollment.query.filter_by(user_id=target_user.id).delete()
                
                # Delete the user itself
                db.session.delete(target_user)
                db.session.commit()
                
                flash(f'User "{username}" deletion approved and account deleted successfully.', 'success')
                return redirect(url_for('manage_user_deletion_requests'))
                
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while deleting the user. Please try again.', 'danger')
                return redirect(url_for('review_user_deletion_request', request_id=request_id))
                
        elif action == 'deny':
            # Deny the deletion request
            deletion_request.status = 'denied'
            deletion_request.admin_notes = admin_notes
            deletion_request.reviewed_by = admin_user.id
            deletion_request.reviewed_at = datetime.utcnow()
            
            db.session.commit()
            flash('User account deletion request denied successfully.', 'success')
            return redirect(url_for('manage_user_deletion_requests'))
    
    return render_template('admin/review_user_deletion_request.html', 
                         user=admin_user,
                         deletion_request=deletion_request) 