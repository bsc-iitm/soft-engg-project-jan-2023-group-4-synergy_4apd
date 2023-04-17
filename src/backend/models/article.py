from backend.database import db
from backend.utils import create_uuid

from sqlalchemy.sql import func


class Article(db.Model):
    __tablename__ = 'article'
    
    id = db.Column(db.String, primary_key=True, default=create_uuid)

    creator = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, default=func.now)
    updated_at = db.Column(db.DateTime, default=func.now)

    tags = db.relationship('Tag', secondary='articles_tags', backref=db.backref('article', lazy='dynamic'))
