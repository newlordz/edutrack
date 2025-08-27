#!/usr/bin/env python3
"""
Create a clean, single quiz result for the user
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Course, Quiz, QuizQuestion, QuizAttempt, QuizAnswer, Grade, Enrollment
from datetime import datetime

def create_clean_quiz_result():
    """Create a clean quiz result"""
    print("=== CREATING CLEAN QUIZ RESULT ===")
    
    with app.app_context():
        try:
            # Get student and quiz
            student = User.query.filter_by(username='student').first()
            quiz = Quiz.query.filter_by(title='Food and Drink Quiz').first()
            
            if not student:
                print("❌ Student not found!")
                return
                
            if not quiz:
                print("❌ Food and Drink Quiz not found!")
                return
            
            print(f"Student: {student.username} (ID: {student.id})")
            print(f"Quiz: {quiz.title} (ID: {quiz.id})")
            
            # Check enrollment
            enrollment = Enrollment.query.filter_by(
                user_id=student.id,
                course_id=quiz.course_id
            ).first()
            
            if not enrollment:
                print("❌ Student not enrolled in course!")
                return
            
            print(f"✅ Student enrolled in course")
            
            # Get questions
            questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
            print(f"✅ Found {len(questions)} questions")
            
            # Create a realistic quiz result (2 out of 3 correct = 66.7%)
            print("\n📝 Creating quiz result...")
            
            score = 2  # 2 out of 3 correct
            max_score = len(questions)
            
            # Create attempt
            attempt = QuizAttempt(
                quiz_id=quiz.id,
                user_id=student.id,
                max_score=max_score,
                completed_at=datetime.now()
            )
            db.session.add(attempt)
            db.session.flush()
            
            print(f"✅ Created attempt (ID: {attempt.id})")
            
            # Process answers (simulate getting 2 out of 3 correct)
            simulated_answers = ['A', 'A', 'C']  # A, A, C (2 correct)
            
            for i, question in enumerate(questions):
                selected_answer = simulated_answers[i]
                is_correct = selected_answer == question.correct_answer
                points_earned = 1 if is_correct else 0
                
                answer = QuizAnswer(
                    attempt_id=attempt.id,
                    question_id=question.id,
                    selected_answer=selected_answer,
                    is_correct=is_correct,
                    points_earned=points_earned
                )
                db.session.add(answer)
                
                print(f"   Q{i+1}: Selected {selected_answer}, Correct {question.correct_answer}, Points: {points_earned}")
            
            # Calculate final score
            attempt.score = score
            attempt.percentage = (score / max_score) * 100
            attempt.passed = attempt.percentage >= quiz.passing_score
            
            print(f"✅ Final score: {score}/{max_score} ({attempt.percentage:.1f}%)")
            print(f"   Passed: {attempt.passed}")
            
            # Create a Grade record
            grade = Grade(
                user_id=student.id,
                course_id=quiz.course_id,
                assignment_name=f"Quiz: {quiz.title}",
                score=attempt.percentage,
                max_score=100.0,
                feedback=f"Quiz completed with {score}/{max_score} correct answers",
                graded_at=datetime.now()
            )
            db.session.add(grade)
            
            print("✅ Created grade record")
            
            # Commit everything
            try:
                db.session.commit()
                print("✅ All data committed successfully!")
                
                # Verify
                final_attempt = QuizAttempt.query.get(attempt.id)
                final_grade = Grade.query.filter_by(assignment_name=f"Quiz: {quiz.title}").first()
                
                print(f"\n📊 VERIFICATION:")
                print(f"   Quiz Attempt: {final_attempt.id} - Score: {final_attempt.score}/{final_attempt.max_score}")
                print(f"   Grade Record: {final_grade.id} - Score: {final_grade.score}%")
                
                print("\n🎯 Now refresh the grades page - you should see only ONE clean result!")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error committing: {e}")
                import traceback
                traceback.print_exc()
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_clean_quiz_result()
