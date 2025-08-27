#!/usr/bin/env python3
"""
Test the new quiz creation system with correct answer specification
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from routes import parse_quiz_text

def test_quiz_parsing():
    """Test the new quiz parsing system"""
    print("=== TESTING NEW QUIZ SYSTEM ===")
    
    # Test quiz text with correct answers
    test_quiz = """Test Quiz

What is 2 + 2?
A) 3
B) 4 [CORRECT]
C) 5
D) 6

What color is the sky?
A) Red
B) Green
C) Blue [CORRECT]
D) Yellow

Which planet is closest to the Sun?
A) Venus
B) Earth
C) Mars
D) Mercury [CORRECT]"""
    
    print("Testing quiz text:")
    print(test_quiz)
    print("\n" + "="*50 + "\n")
    
    # Parse the quiz
    try:
        quiz_data = parse_quiz_text(test_quiz)
        
        print("✅ Quiz parsed successfully!")
        print(f"Title: {quiz_data['title']}")
        print(f"Number of questions: {len(quiz_data['questions'])}")
        
        print("\nQuestions and answers:")
        for i, question in enumerate(quiz_data['questions']):
            print(f"\nQuestion {i+1}: {question['question_text']}")
            print(f"Options:")
            for option, text in question['options'].items():
                marker = " ✅" if option == question['correct_answer'] else ""
                print(f"  {option}) {text}{marker}")
            print(f"Correct answer: {question['correct_answer']}")
        
        # Test validation
        print("\n" + "="*50)
        print("Testing validation...")
        
        all_have_correct_answers = all(q['correct_answer'] for q in quiz_data['questions'])
        if all_have_correct_answers:
            print("✅ All questions have correct answers specified!")
        else:
            print("❌ Some questions are missing correct answers!")
            
    except Exception as e:
        print(f"❌ Error parsing quiz: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== END TEST ===")

if __name__ == "__main__":
    test_quiz_parsing()
