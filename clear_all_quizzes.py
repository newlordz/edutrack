#!/usr/bin/env python3
"""
Script to clear all quiz-related data from the database
This will remove all quizzes, questions, attempts, and answers
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def clear_all_quizzes():
    """Clear all quiz-related data from the database"""
    try:
        from app import app
        from database import db
        from models import Quiz, QuizQuestion, QuizAttempt, QuizAnswer
        from sqlalchemy import text
        
        with app.app_context():
            print("🧹 Clearing all quiz data...")
            
            # Get counts before deletion
            quiz_count = Quiz.query.count()
            question_count = QuizQuestion.query.count()
            attempt_count = QuizAttempt.query.count()
            answer_count = QuizAnswer.query.count()
            
            print(f"📊 Current quiz data:")
            print(f"   - Quizzes: {quiz_count}")
            print(f"   - Questions: {question_count}")
            print(f"   - Attempts: {attempt_count}")
            print(f"   - Answers: {answer_count}")
            
            if quiz_count == 0:
                print("✅ No quiz data to clear!")
                return True
            
            # Delete in correct order (respecting foreign key constraints)
            print("\n🗑️  Deleting quiz data...")
            
            # Delete answers first
            if answer_count > 0:
                deleted_answers = QuizAnswer.query.delete()
                print(f"   ✓ Deleted {deleted_answers} quiz answers")
            
            # Delete attempts
            if attempt_count > 0:
                deleted_attempts = QuizAttempt.query.delete()
                print(f"   ✓ Deleted {deleted_attempts} quiz attempts")
            
            # Delete questions
            if question_count > 0:
                deleted_questions = QuizQuestion.query.delete()
                print(f"   ✓ Deleted {deleted_questions} quiz questions")
            
            # Delete quizzes
            if quiz_count > 0:
                deleted_quizzes = Quiz.query.delete()
                print(f"   ✓ Deleted {deleted_quizzes} quizzes")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ All quiz data cleared successfully!")
            
            # Verify deletion
            remaining_quizzes = Quiz.query.count()
            remaining_questions = QuizQuestion.query.count()
            remaining_attempts = QuizAttempt.query.count()
            remaining_answers = QuizAnswer.query.count()
            
            print(f"\n📊 Verification:")
            print(f"   - Remaining quizzes: {remaining_quizzes}")
            print(f"   - Remaining questions: {remaining_questions}")
            print(f"   - Remaining attempts: {remaining_attempts}")
            print(f"   - Remaining answers: {remaining_answers}")
            
            if all(count == 0 for count in [remaining_quizzes, remaining_questions, remaining_attempts, remaining_answers]):
                print("\n🎉 Database is now completely clean and ready for new quizzes!")
            else:
                print("\n⚠️  Some data may still remain. Check the verification above.")
            
            return True
            
    except Exception as e:
        print(f"❌ Error clearing quiz data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧹 Quiz Data Cleaner")
    print("=" * 50)
    
    # Automatically clear all quiz data
    print("Automatically clearing all quiz data...")
    success = clear_all_quizzes()
    
    if success:
        print("\n✅ Quiz clearing completed successfully!")
    else:
        print("\n❌ Quiz clearing failed!")
