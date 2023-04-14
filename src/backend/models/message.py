# Author: Adhil

from backend.database import db
from datetime import datetime
import uuid


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column("id", db.String, primary_key=True, default=str(uuid.uuid4()))
    text = db.Column("text", db.String, nullable=False)
    sender_id = db.Column("sender_id", db.String, db.ForeignKey("user.id"))
    ticket_id = db.Column("ticket_id", db.String, db.ForeignKey("ticket.id"))
    hidden = db.Column("hidden", db.Boolean)
    posted_at = db.Column("posted_at", db.DateTime, default=datetime.now())
    flagged = db.Column("flagged", db.Boolean, nullable=False)
