from models import db
from models.question import question_quiz
from models.student import student_quiz
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer

class Quiz(db.Model):
    id = Column(String(120), primary_key=True)
    teacher_id = Column(String(120), ForeignKey('teacher.id'), nullable=False)
    duration = Column(Integer, nullable=False)
    code = Column(String(120))
    subject = Column(String(120))
    doc = Column(String(240), nullable=True)
    pdf = Column(String(240))

    # relationships
    teacher = relationship('Teacher', back_populates='quizs')
    questions = relationship('Question', secondary=question_quiz, back_populates='quizs')
    students = relationship('Student', secondary=student_quiz, back_populates='quizs')
    scores = relationship('Score', back_populates='quiz')