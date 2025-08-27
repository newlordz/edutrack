# 🎯 Quiz System - EduTrack

A simple and powerful quiz system that allows teachers to create quizzes using plain text and students to take them with automatic grading.

## ✨ Features

- **Simple Text Input**: Teachers can create quizzes by typing questions in a simple format
- **Automatic Parsing**: The system automatically converts text to structured quiz questions
- **Multiple Choice**: Support for A, B, C, D multiple choice questions
- **Automatic Grading**: Instant results with detailed feedback
- **Progress Tracking**: Students can only take each quiz once
- **Beautiful UI**: Modern, responsive interface for both teachers and students

## 🚀 Quick Start

### 1. Setup Database Tables

Run the database migration script to create quiz tables:

```bash
cd EduTrack
python create_quiz_tables.py
```

### 2. Create a Quiz (Teachers)

1. Go to your course dashboard
2. Click "Create Quiz" button
3. Enter quiz content in this format:

```
Basic Science Quiz

What is the chemical symbol for the element gold?
A) Au
B) Ag
C) Gd
D) Fe

What is the process by which plants make their own food using sunlight?
A) Respiration
B) Transpiration
C) Photosynthesis
D) Germination

Which of the following is the largest organ in the human body?
A) Heart
B) Brain
C) Liver
D) Skin
```

4. Set time limit and passing score
5. Click "Create Quiz"

### 3. Take a Quiz (Students)

1. Go to the course page
2. Find the quiz in the "Quizzes" section
3. Click "Take Quiz"
4. Answer all questions
5. Submit and view results

## 📝 Quiz Format Rules

### Required Format:
- **First line**: Quiz title
- **Questions**: Must end with a question mark (?)
- **Options**: Must start with A), B), C), D)
- **Spacing**: Use blank lines to separate questions

### Example:
```
Quiz Title

Question 1?
A) Option A
B) Option B
C) Option C
D) Option D

Question 2?
A) Option A
B) Option B
C) Option C
D) Option D
```

## ⚠️ Important Notes

- **Correct Answer**: The first option (A) is automatically marked as correct
- **One Attempt**: Students can only take each quiz once
- **Time Limit**: Set appropriate time limits for your quizzes
- **Passing Score**: Default is 70% but can be customized

## 🔧 Technical Details

### Database Tables:
- `quiz`: Main quiz information
- `quiz_question`: Individual questions and options
- `quiz_attempt`: Student quiz attempts
- `quiz_answer`: Student answers and grading

### Routes:
- `/quiz/create/<course_id>`: Create new quiz
- `/quiz/<quiz_id>/take`: Take a quiz
- `/quiz/results/<attempt_id>`: View quiz results

### Models:
- `Quiz`: Quiz metadata and settings
- `QuizQuestion`: Question text and options
- `QuizAttempt`: Student attempt tracking
- `QuizAnswer`: Answer validation and scoring

## 🎨 Customization

### Styling:
- All templates use Bootstrap 5
- Custom CSS for enhanced visual appeal
- Responsive design for mobile devices

### Features:
- Easy to extend with additional question types
- Can add timer functionality
- Can implement question randomization
- Can add question categories/tags

## 🐛 Troubleshooting

### Common Issues:

1. **"No valid questions found"**
   - Check that questions end with question marks (?)
   - Ensure options start with A), B), C), D)
   - Verify proper spacing between questions

2. **Database errors**
   - Run `python create_quiz_tables.py`
   - Check database connection
   - Verify model imports

3. **Template errors**
   - Check that all templates are in the correct location
   - Verify route registrations in `app.py`
   - Check for syntax errors in HTML templates

## 📚 Future Enhancements

- [ ] Question randomization
- [ ] Timer countdown
- [ ] Question categories
- [ ] Essay questions
- [ ] File upload questions
- [ ] Quiz analytics
- [ ] Question bank
- [ ] Quiz templates

## 🤝 Contributing

To add new features or fix bugs:

1. Update the models if needed
2. Add new routes in `routes.py`
3. Create/update HTML templates
4. Test thoroughly
5. Update this documentation

---

**Happy Quizzing! 🎓**
