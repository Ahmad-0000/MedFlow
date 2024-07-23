#!/usr/bin/python3
"""
Contains main questions model
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    """Main question model"""
    __tablename__ = "questions"
    user_id = Column(String(40), ForeignKey('users.id'), nullable=False)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    user = relationship('User', back_populates='questions')
    answers = relationship('Answer', back_populates='question',
                           cascade="all, delete, delete-orphan")
    comments = relationship('QueComment', back_populates='question',
                            cascade="all, delete, delete-orphan")
