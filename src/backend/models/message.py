# Author: Adhil

from backend.database import db
from sqlalchemy import String, Column, Integer, ForeignKey, Boolean, DateTime
from datetime import datetime

class Message(db.Model):
    __tablename__ = "message"

    id = Column("id", Integer(), primary_key = True)
    text = Column("text", String(), nullable = False)
    sender_id = Column("sender_id", Integer(), ForeignKey("user.id"))
    ticket_id = Column("ticket_id", Integer(), ForeignKey("ticket.id"))
    hidden = Column("hidden", Boolean(), nullable = False)
    posted_at = Column("posted_at", DateTime(), default = datetime.now())
    flagged = Column("flagged", Boolean(), nullable = False)