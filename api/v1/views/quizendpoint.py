import uuid
from random import shuffle
from models import db
from models.question import Question
from models.student import Student
from models.quiz import Quiz
from models.teacher import Teacher
from models.score import Score
from api.v1.views import app_views, needed, question_options
from flask import Flask, request, abort, jsonify

@app_views.route('/verify/<id>', methods=['POST'])
def verify_student(id):
    """verify student"""
    code = request.get_json()
    if not code:
        abort(404)
    quiz = db.get_or_404(Quiz, id)
    if quiz.code == code:
        return jsonify({'isVerified': True})
    else:
        return jsonify({'isVerified': False})
    
@app_views.route('/register/<id>', methods=['POST'])
def register_student(id):
    """registers student to the database
    and sends student's quiz questions"""
    student_names = request.get_json()
    print(student_names)
    if not student_names:
        abort(404)
    firstname = student_names.get('firstName')
    lastname = student_names.get('LastName')
    email = student_names.get('Email')
    print(email)
    print(firstname)
    print(lastname)
    if not firstname or not lastname:
        abort(404)

    quiz = db.get_or_404(Quiz, id)
    student = db.session.execute(db.select(Student).filter_by(email=email)).first()

    
    if not student:
        student = Student(id=uuid.uuid4(),
                          email= email,
                          firstname=firstname,
                          lastname=lastname)
        student.teachers.append(quiz.teacher)
        student.quizs.append(quiz)
        quiz.students.append(student)
        db.session.add(student)
        db.session.commit()
    else:
        student = student[0]
        if student not in quiz.students:
            quiz.students.append(student)
            db.session.commit()


    # sending the questions that student will answer
    quiz_questions = {}
    quiz_questions['Subject'] = quiz.subject
    quiz_questions['duration'] = quiz.duration
    questions = quiz.questions
    questions_list = []
    for question in questions:
        new_dict = {}
        options = []
        for key, value in question.__dict__.items():
            if key in needed:
                new_dict[key] = value
            if key in question_options:
                options.append(value)
        shuffle(options)
        new_dict['options'] = options
        questions_list.append(new_dict)
    print(questions_list)
    quiz_questions['questions'] = questions_list

    return jsonify({'id': student.id, 'isRegistered': True, 'testQuestions': quiz_questions})



@app_views.route('/calculate-score/<id>', methods=['POST'])
def calculate_score(id):
    score_metadata = request.get_json()
    if not score_metadata:
        abort(404)
    score_list = score_metadata.get('quiz')
    student_id = score_metadata.get('studentId')
    quiz = db.get_or_404(Quiz, id)
    score = 0
    for answer_dict in score_list:
        question_id = answer_dict['questionId']
        selected_option = answer_dict['selectedOption']
        question = db.get_or_404(Question, question_id)
        
        if selected_option == question.right_answer:
            score += 1
    score = int((score / len(quiz.questions)) * 100)
    score_model = Score(
        id=uuid.uuid4(),
        student_id=student_id,
        quiz_id = quiz.id,
        score=score
    )
    db.session.add(score_model)
    db.session.commit()
    return jsonify({'status': 'submitted'})
        



@app_views.route('/teacher-quiz/<id>', methods=['GET'])
def get_teacher_quiz(id):
    """gets the all the quiz that a.
    teacher created"""
    teacher = db.get_or_404(Teacher, id)
    if not teacher:
        abort(404)
    quizs = teacher.quizs
    # quiz_dict = {}
    # for quiz_obj in quizs:
    #     questions = quiz_obj.questions
    #     questions_list = []
    #     for question in questions:
    #         new_dict = {}
    #         for key, value in question.__dict__.items():
    #             if key in needed:
    #                 new_dict[key] = value   
    #         questions_list.append(new_dict)
    #     quiz_dict[quiz_obj.id] = questions_list
    quiz_ids = [quiz.id for quiz in quizs]
    print(quizs)
    return jsonify(quiz_ids)

@app_views.route('/quiz-details/<id>')
def get_quiz_details(id):
    """gets the quiz info"""

    quiz = db.get_or_404(Quiz, id)
    questions = quiz.questions
    questions_list = []
    for question in questions:
        new_dict = {}
        for key, value in question.__dict__.items():
            if key in needed:
                new_dict[key] = value   
        questions_list.append(new_dict)
    return_dict = {}
    return_dict['docFile'] = quiz.doc
    return_dict['questions'] = questions_list
    return_dict['excelScoreFile'] = f'/download-studentscore/{id}'

    return jsonify(return_dict)

    
