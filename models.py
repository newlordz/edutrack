from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, teacher, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    submissions = db.relationship('AssignmentSubmission', 
                                foreign_keys='AssignmentSubmission.user_id',
                                backref='student', lazy=True)
    graded_submissions = db.relationship('AssignmentSubmission',
                                       foreign_keys='AssignmentSubmission.graded_by',
                                       backref='grader', lazy=True)
    study_progress = db.relationship('StudyProgress', backref='student', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_enrolled_courses(self):
        return [enrollment.course for enrollment in self.enrollments]
    
    def get_course_progress(self, course_id):
        """Calculate progress based on completed materials"""
        # Get total materials for the course
        total_materials = CourseMaterial.query.filter_by(course_id=course_id).count()
        if total_materials == 0:
            return 0
        
        # Get completed materials
        completed_materials = StudyProgress.query.filter_by(
            user_id=self.id,
            course_id=course_id,
            completion_status='completed'
        ).count()
        
        return (completed_materials / total_materials) * 100
    
    def __repr__(self):
        return f'<User {self.username}>'

class Quiz(db.Model):
    __tablename__ = 'quiz'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    time_limit_minutes = db.Column(db.Integer, default=30)
    passing_score = db.Column(db.Integer, default=70)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class QuizQuestion(db.Model):
    __tablename__ = 'quiz_question'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    points = db.Column(db.Integer, default=1)
    order_num = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<QuizQuestion {self.id}>'

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempt'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    max_score = db.Column(db.Float, default=0.0)
    percentage = db.Column(db.Float, default=0.0)
    passed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='quiz_attempts', lazy=True)
    answers = db.relationship('QuizAnswer', backref='attempt', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<QuizAttempt {self.id}>'

class QuizAnswer(db.Model):
    __tablename__ = 'quiz_answer'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    is_correct = db.Column(db.Boolean, default=False)
    points_earned = db.Column(db.Float, default=0.0)
    
    # Relationships
    question = db.relationship('QuizQuestion', backref='answers', lazy=True)
    
    def __repr__(self):
        return f'<QuizAnswer {self.id}>'

class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to teacher
    duration_weeks = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    max_students = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)
    materials = db.relationship('CourseMaterial', backref='course', lazy=True)
    announcements = db.relationship('Announcement', backref='course', lazy=True)
    assignments = db.relationship('Assignment', backref='course', lazy=True)
    quizzes = db.relationship('Quiz', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def get_enrolled_count(self):
        return len(self.enrollments)
    
    def is_full(self):
        return self.get_enrolled_count() >= self.max_students
    
    def get_average_grade(self):
        valid_grades = [grade.score for grade in self.grades if grade.score is not None and grade.score >= 0]
        if not valid_grades:
            return 0.0
        return round(sum(valid_grades) / len(valid_grades), 2)
    
    def __repr__(self):
        return f'<Course {self.title}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Float, default=0.0)  # Percentage (0-100)
    status = db.Column(db.String(20), default='active')  # active, completed, dropped
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id'),)
    
    def __repr__(self):
        return f'<Enrollment User:{self.user_id} Course:{self.course_id}>'

class Grade(db.Model):
    __tablename__ = 'grade'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    assignment_name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float)  # Percentage (0-100)
    max_score = db.Column(db.Float, default=100.0)
    feedback = db.Column(db.Text)
    graded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_letter_grade(self):
        if self.score is None:
            return 'N/A'
        elif self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    def __repr__(self):
        return f'<Grade {self.assignment_name}: {self.score}>'

class CourseMaterial(db.Model):
    __tablename__ = 'course_material'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))  # pdf, video, document, etc.
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_index = db.Column(db.Integer, default=0)  # For organizing materials in sequence
    
    def __repr__(self):
        return f'<CourseMaterial {self.title}>'

class Announcement(db.Model):
    __tablename__ = 'announcement'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

class Assignment(db.Model):
    __tablename__ = 'assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    max_score = db.Column(db.Float, default=100.0)
    assignment_type = db.Column(db.String(50), default='assignment')  # assignment, quiz, exam
    instructions = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    submissions = db.relationship('AssignmentSubmission', backref='assignment', lazy=True)
    
    def __repr__(self):
        return f'<Assignment {self.title}>'

class AssignmentSubmission(db.Model):
    __tablename__ = 'assignment_submission'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submission_text = db.Column(db.Text)
    file_path = db.Column(db.String(500))  # For file uploads
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)  # Graded score
    feedback = db.Column(db.Text)  # Teacher feedback
    graded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    graded_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='submitted')  # submitted, graded, late
    
    def is_late(self):
        if self.assignment and self.assignment.due_date:
            return self.submitted_at > self.assignment.due_date
        return False
    
    def __repr__(self):
        return f'<AssignmentSubmission {self.assignment_id}:{self.user_id}>'

class StudyProgress(db.Model):
    __tablename__ = 'study_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('course_material.id'), nullable=False)
    study_time_minutes = db.Column(db.Integer, default=0)
    completion_status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)  # Student's personal notes
    
    __table_args__ = (db.UniqueConstraint('user_id', 'material_id'),)
    
    def __repr__(self):
        return f'<StudyProgress User:{self.user_id} Material:{self.material_id}>'

class CourseDeletionRequest(db.Model):
    __tablename__ = 'course_deletion_request'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Teacher who requested
    reason = db.Column(db.Text, nullable=False)  # Why they want to delete the course
    status = db.Column(db.String(20), default='pending')  # pending, approved, denied
    admin_notes = db.Column(db.Text)  # Admin's notes when approving/denying
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who reviewed
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    course = db.relationship('Course', backref='deletion_requests')
    requester = db.relationship('User', foreign_keys=[requested_by], backref='deletion_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_deletions')
    
    def __repr__(self):
        return f'<CourseDeletionRequest Course:{self.course_id} Status:{self.status}>'

class UserDeletionRequest(db.Model):
    __tablename__ = 'user_deletion_request'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)  # Why they want to delete their account
    status = db.Column(db.String(20), default='pending')  # pending, approved, denied
    admin_notes = db.Column(db.Text)  # Admin's notes when approving/denying
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who reviewed
    reviewed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='account_deletion_requests')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='reviewed_account_deletions')
    
    def __repr__(self):
        return f'<UserDeletionRequest User:{self.user_id} Status:{self.status}>'
