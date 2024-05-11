from models import db
from models.teacher import Teacher
from api.v1.views import app_views, needed, question_options
from flask import jsonify
from datetime import datetime
from utils import convert_date_to_string

@app_views.route('activities_total/<teacher_id>')
def get_totals(teacher_id):
    """gets the totals for a teacher based on the month and year"""

    teacher = db.get_or_404(Teacher, teacher_id)

    # gets all students, quiz, and questions connected to the teacher
    students = teacher.students
    quizs = teacher.quizs
    questions = teacher.questions

    # gets the unique month and year for students, quiz, and questions
    student_months = set([convert_date_to_string(data.created_at) for data in students])
    quizs_months = set([convert_date_to_string(data1.created_at) for data1 in quizs])
    questions_months = set([convert_date_to_string(data2.created_at) for data2 in questions])

    month_year_array = student_months.union(quizs_months).union(questions_months)
    month_year_array = list(month_year_array)
    month_year_array.sort(key= lambda x: datetime.strptime(x, '%b %y'))
    if len(month_year_array) > 12:
        month_year_array = month_year_array[:12]
    else:
        month_year_array = month_year_array
    return_list = []
    for month_year in month_year_array:
        month_total_info = {} # gets information on the particular month and the quiz, question and student totals for that month
        month = month_year.split(' ')[0]
        year = month_year.split(' ')[1]
        student_list = []
        for student in students:
            if student.created_at.strftime('%b') == month and student.created_at.strftime('%y') == year:
                student_list.append(student)
        quiz_list = []
        for quiz in quizs:
            if quiz.created_at.strftime('%b') == month and quiz.created_at.strftime('%y') == year:
                quiz_list.append(quiz)

        question_list = []
        for question in questions:
            if question.created_at.strftime('%b') == month and question.created_at.strftime('%y') == year:
                question_list.append(question)

        month_total_info['month'] = month_year
        month_total_info['totalStudents'] = len(student_list)
        month_total_info['totalQuizzes'] = len(quiz_list)
        month_total_info['totalQuestions'] = len(question_list)
        return_list.append(month_total_info)


        
    # teacher_totals = {}
    # teacher_totals['students'] = len(teacher.students)
    # teacher_totals['quizes'] = len(teacher.quizs)
    # teacher_totals['questions'] = len(teacher.questions)

    return jsonify(return_list)