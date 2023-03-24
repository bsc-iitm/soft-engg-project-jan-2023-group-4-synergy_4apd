# Author: Afnan
from backend.database import db

from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True)
    title = Column(String(25), nullable=False)

    status = Column(Integer, default=0)
    votes = Column(Integer, default=0)
    is_public = Column(Boolean)

    creator = Column(Integer, ForeignKey('user.id'), nullable=False)
    assignee = Column(Integer, ForeignKey('user.id'), nullable=False)

    solution = Column(Integer, ForeignKey('message.id'), nullable=False)

    last_response_time = Column(DateTime, default=func.now())

    tags = relationship('Tag', secondary='tickets_tags')