#!/usr/bin/python3
"""
Contains main tags model
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Table
from sqlalchemy.orm import relationship
from models.question import questions_tags


class Tag(BaseModel, Base):
    """Represent tags model"""
    __tablename__ = "tags"
    name = Column(String(30), nullable=False)
    questions = relationship("Question", secondary=questions_tags,
                             back_populates="tags")
