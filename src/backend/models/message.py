# Author: Adhil

from backend.database import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column("id", db.Integer, primary_key=True)
    text = db.Column("text", db.String, nullable=False)
    sender_id = db.Column("sender_id", db.Integer, db.ForeignKey("user.id"))
    ticket_id = db.Column("ticket_id", db.Integer, db.ForeignKey("ticket.id"))
    hidden = db.Column("hidden", db.Boolean)
    posted_at = db.Column("posted_at", db.DateTime, default=datetime.now())
    flagged = db.Column("flagged", db.Boolean, nullable=False)
