"""
Contains main answers model
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Text, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Answer(BaseModel, Base):
    """Main answers model"""
    __tablename__ = "answers"
    user_id = Column(String(40), ForeignKey('users.id'), nullable=False)
    question_id = Column(String(40), ForeignKey('questions.id'),
                         nullable=False)
    body = Column(Text, nullable=False)
    user = relationship('User', back_populates='answers')
    question = relationship('Question', back_populates="answers")
    comments = relationship('AnsComment', back_populates='answer',
                            cascade="all, delete, delete-orphan")