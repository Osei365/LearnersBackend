import uuid
from models import db
from models.teacher import Teacher
from models.student import Student
from api.v1.views import app_views, needed, question_options
from flask import jsonify

@app_views.route('/get-students/<id>', methods=['GET'])
def get_students(id):
    """gets all students that registered with a
    particular teacher"""

    teacher = db.get_or_404(Teacher, id)
    teacher_quizs= [quiz for quiz in teacher.quizs]
    students = teacher.students
    students_list = []
    for student in students:
        students_dictionary = {}
        students_dictionary['firstname'] = student.firstname
        students_dictionary['lastname'] = student.lastname
        student_quizs = [quiz for quiz in student.quizs if quiz in teacher_quizs]
        print(student_quizs)
        student_scores = [score.score for score in student.scores if score.quiz in student_quizs]
        print(student_scores)
        students_dictionary['quizTaken'] = len(student_quizs)
        if len(student_scores) > 0:
            students_dictionary['averageScore'] = sum(student_scores)/len(student_scores)
        else:
            students_dictionary['averageScore']  = 0
        students_list.append(students_dictionary)
    return jsonify(students_list)

@app_views.route('/get-students', methods=['GET'])
def getAllStudents():
    """get all students"""

    students = db.session.execute(db.select(Student)).all()
    return jsonify({'totalStudents': len(students)})