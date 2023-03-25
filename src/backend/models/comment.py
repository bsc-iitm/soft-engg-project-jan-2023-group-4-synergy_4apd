# Author: Adhil

from backend.database import db


class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column("id", db.Integer, primary_key = True)
    article_id = db.Column("article_id", db.Integer, db.ForeignKey("article.id"))
    hidden = db.Column("hidden", db.Boolean)
    content = db.Column("content", db.String, nullable = False)