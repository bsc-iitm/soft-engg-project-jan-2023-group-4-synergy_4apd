from backend.database import db


tickets_tags = db.Table('tickets_tags',
                       db.Column('ticket_id', db.String, db.ForeignKey('ticket.id')),
                       db.Column('tag_id', db.String, db.ForeignKey('tag.id'))
                       )
