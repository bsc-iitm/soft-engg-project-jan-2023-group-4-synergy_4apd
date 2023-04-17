from backend.database import db
from backend.utils import create_uuid

from sqlalchemy.sql import func


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    content = db.Column(db.String, nullable=False)
    posted_at = db.Column(db.DateTime, default=func.now())

    article_id = db.Column(db.String, db.ForeignKey('article.id'))

    hidden = db.Column(db.Boolean, default=False)
