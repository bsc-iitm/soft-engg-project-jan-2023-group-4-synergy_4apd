from backend.database import db
from backend.utils import create_uuid


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    content = db.Column(db.String, nullable=False)

    article_id = db.Column(db.String, db.ForeignKey('article.id'))

    hidden = db.Column(db.Boolean, default=False)
