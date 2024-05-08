from flask import Blueprint

needed = ['id', 'teacher_id', 'subject', 'header',
          'body', 'image']
question_options = ['right_answer', 'wrong_answer1','wrong_answer2', 
                    'wrong_answer3','wrong_answer4']
app_views = Blueprint('app_views', __name__, url_prefix='/api/learners/v1')

from api.v1.views.signup import *
from api.v1.views.login import *
from api.v1.views.allquestions import *
from api.v1.views.quizendpoint import *
from api.v1.views.images_api import *
from api.v1.views.studentendpoint import *
from api.v1.views.documents_api import *
from api.v1.views.student_score_api import *
from api.v1.views.update_name import *
from api.v1.views.update_password import *
from api.v1.views.teacher_details import *