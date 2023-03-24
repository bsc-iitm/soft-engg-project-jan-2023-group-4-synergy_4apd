# Author: Afnan

from backend.database import db

from sqlalchemy import Column, Integer, ForeignKey


class TicketsTags(db.Model):
    __tablename__ = 'tickets_tags'

    id = Column(Integer, primary_key=True)
    ticket_id = Column('ticket_id', Integer, ForeignKey('ticket.id'))
    tag_id = Column('tag_id', Integer, ForeignKey('tag.id'))
