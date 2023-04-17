from backend.database import db
from backend.utils import create_uuid

from sqlalchemy.sql import func

class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    sender_id = db.Column(db.String, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.String, db.ForeignKey('user.id'))

    content = db.Column(db.String, nullable=True)
    action_url = db.Column(db.String, nullable=True)
    
    timestamp = db.Column(db.DateTime, default=func.now())
    
    read = db.Column(db.Boolean, default=False)