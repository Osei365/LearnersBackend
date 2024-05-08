from models import db, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer


class Score(db.Model):
    """scores of students for quizs"""
    id = Column(String(120), primary_key=True)
    student_id = Column(String(120), ForeignKey('student.id'))
    quiz_id = Column(String(120), ForeignKey('quiz.id'))
    score = Column(Integer, nullable=False)


    student = relationship('Student', back_populates='scores')
    quiz = relationship('Quiz', back_populates='scores')