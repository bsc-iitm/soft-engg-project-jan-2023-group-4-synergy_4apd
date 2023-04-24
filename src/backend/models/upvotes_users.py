from backend.database import db

upvotes_users = db.Table('upvotes_users',
                       db.Column('ticket_id', db.String, db.ForeignKey('ticket.id')),
                       db.Column('user_id', db.String, db.ForeignKey('user.id'))
                       )