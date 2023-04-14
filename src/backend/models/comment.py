# Author: Adhil

from backend.database import db
import uuid


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column("id", db.String, primary_key = True, default=str(uuid.uuid4()))
    article_id = db.Column("article_id", db.Integer, db.ForeignKey("article.id"))
    hidden = db.Column("hidden", db.Boolean)
    content = db.Column("content", db.String, nullable = False)