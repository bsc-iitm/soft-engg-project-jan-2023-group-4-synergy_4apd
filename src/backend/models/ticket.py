from backend.database import db
from backend.utils import create_uuid

from sqlalchemy.sql import func


class Ticket(db.Model):
    __tablename__ = 'ticket'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    title = db.Column(db.String, nullable=False)

    status = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=False)

    creator = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    assignee = db.Column(db.String, db.ForeignKey('user.id'))

    solution = db.Column(db.String, db.ForeignKey('message.id'))

    last_response_time = db.Column(db.DateTime, default=func.now())

    tags = db.relationship('Tag', secondary='tickets_tags', backref=db.backref('ticket', lazy='dynamic'))
