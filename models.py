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
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_enrolled_courses(self):
        return [enrollment.course for enrollment in self.enrollments]
    
    def get_course_progress(self, course_id):
        enrollment = Enrollment.query.filter_by(user_id=self.id, course_id=course_id).first()
        return enrollment.progress if enrollment else 0
    
    def __repr__(self):
        return f'<User {self.username}>'

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
