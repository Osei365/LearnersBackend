from models import db, Base
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text

question_quiz = Table(
    'question_quiz',
    Base.metadata,
    Column('question_id', String(120), ForeignKey('question.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('quiz_id', String(120), ForeignKey('quiz.id', onupdate='CASCADE', ondelete='CASCADE'))
)

class Question(db.Model):
    id = Column(String(120), primary_key=True)
    teacher_id = Column(String(120), ForeignKey('teacher.id'), nullable=False) ## one to many relationship
    subject = Column(String(120), nullable=False) 
    header = Column(String(120))
    body = Column(Text)
    image = Column(String(120))
    right_answer = Column(String(120))
    wrong_answer1 = Column(String(120))
    wrong_answer2 = Column(String(120))
    wrong_answer3 = Column(String(120))
    wrong_answer4 = Column(String(120))


    # relationships
    teacher = db.relationship('Teacher')
    quizs = db.relationship('Quiz', secondary=question_quiz, back_populates='questions')

