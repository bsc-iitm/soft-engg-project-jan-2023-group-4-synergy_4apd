# Author: Afnan
from backend.database import db

from sqlalchemy.sql import func

from .tickets_tags import *


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25), nullable=False)

    status = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean)

    creator = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    solution = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)

    last_response_time = db.Column(db.DateTime, default=func.now())

    tags = db.relationship("Tag", secondary=tickets_tags,backref=db.backref("ticket",lazy="dynamic"))