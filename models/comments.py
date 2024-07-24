"""
Contains comments models for answers and questions
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class QueComment(BaseModel, Base):
    """Represents question comment"""
    __tablename__ = "question_comments"
    user_id = Column(String(40), ForeignKey('users.id'), nullable=False)
    question_id = Column(String(40), ForeignKey('questions.id'),
                         nullable=False)
    body = Column(String(300), nullable=False)
    user = relationship('User', back_populates='question_comments')
    question = relationship('Question', back_populates='comments')


class AnsComment(BaseModel, Base):
    """Represents answer comment"""
    __tablename__ = "answer_comments"
    user_id = Column(String(40), ForeignKey('users.id'), nullable=False)
    answer_id = Column(String(40), ForeignKey('answers.id'), nullable=False)
    body = Column(String(300), nullable=False)
    user = relationship('User', back_populates='answer_comments')
    answer = relationship('Answer', back_populates='comments')
