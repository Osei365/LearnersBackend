from models import db
from models.teacher import Teacher
from api.v1.views import app_views, needed, question_options
from flask import jsonify


@app_views.route('activities_total/<teacher_id>')
def get_totals(teacher_id):
    """gets the totals for a teacher"""

    teacher = db.get_or_404(Teacher, teacher_id)
    teacher_totals = {}
    teacher_totals['students'] = len(teacher.students)
    teacher_totals['quizes'] = len(teacher.quizs)
    teacher_totals['questions'] = len(teacher.questions)

    return jsonify(teacher_totals)