"""
Contains main users model
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents user's account"""
    __tablename__ = "users"
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(32), nullable=False, unique=True)
    gender = Column(String(1), nullable=True)
    birth_date = Column(Date, nullable=False)
    date_joined = Column(Date, nullable=False)
    education = Column(String(200), nullable=True)
    bio = Column(String(1024), nullable=True)
    questions = relationship('Question', back_populates="user",
                             cascade="all, delete, delete-orphan")
    answers = relationship('Answer', back_populates="user",
                           cascade="all, delete, delete-orphan")
    question_comments = relationship('QueComment', back_populates="user",
                                     cascade="all, delete, delete-orphan")
    answer_comments = relationship('AnsComment', back_populates='user',
                                   cascade='all, delete, delete-orphan')
