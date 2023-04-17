from backend.database import db
from backend.utils import create_uuid

from sqlalchemy.sql import func


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    text = db.Column(db.String, nullable=False)
    posted_at = db.Column(db.DateTime, default=func.now())

    sender_id = db.Column(db.String, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.String, db.ForeignKey('ticket.id'))

    hidden = db.Column(db.Boolean, default=False)
    flagged = db.Column(db.Boolean, default=False)
