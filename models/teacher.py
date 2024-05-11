from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from flask_login import UserMixin
from models.student import student_teacher
from datetime import datetime


class Teacher(db.Model, UserMixin):

    id = Column(String(120), primary_key=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    first_name = Column(String(120), nullable=True)
    last_name = Column(String(120), nullable=True)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    institution = Column(String(120), nullable=True)
    teacher_image = Column(String(120))

    # relationships
    questions = relationship('Question', back_populates='teacher')
    quizs = relationship('Quiz', back_populates='teacher')
    students = relationship('Student', secondary=student_teacher, back_populates='teachers')