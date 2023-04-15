# Author: Afnan
from backend.database import db
from backend.utils import createUUID, setTime
from .tickets_tags import *


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.String, primary_key=True, default=createUUID)
    title = db.Column(db.String(25), nullable=False)

    status = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean)

    creator = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.String, db.ForeignKey('user.id'))

    solution = db.Column(db.String, db.ForeignKey('message.id'))

    last_response_time = db.Column(db.DateTime, default=setTime)

    tags = db.relationship("Tag", secondary=tickets_tags,backref=db.backref("ticket",lazy="dynamic"))