#!/usr/bin/env python3
"""
Test quiz submission to see why grades aren't being saved
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Course, Quiz, QuizQuestion, QuizAttempt, QuizAnswer, Grade, Enrollment
from datetime import datetime

def test_quiz_submission():
    """Test the quiz submission process"""
    print("=== TESTING QUIZ SUBMISSION ===")
    
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
            
            # Check if already attempted
            existing_attempt = QuizAttempt.query.filter_by(
                quiz_id=quiz.id,
                user_id=student.id
            ).first()
            
            if existing_attempt:
                print(f"⚠️  Student already attempted this quiz (ID: {existing_attempt.id})")
                print(f"   Score: {existing_attempt.score}/{existing_attempt.max_score} ({existing_attempt.percentage}%)")
                return
            
            print("✅ No previous attempts found")
            
            # Simulate quiz submission
            print("\n📝 Simulating quiz submission...")
            
            # Create attempt
            attempt = QuizAttempt(
                quiz_id=quiz.id,
                user_id=student.id,
                max_score=len(quiz.questions),
                completed_at=datetime.now()
            )
            db.session.add(attempt)
            db.session.flush()
            
            print(f"✅ Created attempt (ID: {attempt.id})")
            
            # Process answers (simulate student getting 2 out of 3 correct)
            score = 0
            questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
            
            # Simulate answers: A, A, C (2 correct out of 3)
            simulated_answers = ['A', 'A', 'C']
            correct_answers = [q.correct_answer for q in questions]
            
            for i, (question, selected_answer) in enumerate(zip(questions, simulated_answers)):
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
                
                print(f"   Q{i+1}: Selected {selected_answer}, Correct {question.correct_answer}, Points: {points_earned}")
            
            # Calculate final score
            attempt.score = score
            attempt.percentage = (score / len(questions)) * 100
            attempt.passed = attempt.percentage >= quiz.passing_score
            
            print(f"✅ Final score: {score}/{len(questions)} ({attempt.percentage:.1f}%)")
            print(f"   Passed: {attempt.passed}")
            
            # Create a Grade record
            grade = Grade(
                user_id=student.id,
                course_id=quiz.course_id,
                assignment_name=f"Quiz: {quiz.title}",
                score=attempt.percentage,
                max_score=100.0,
                feedback=f"Quiz completed with {score}/{len(questions)} correct answers",
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
    test_quiz_submission()
