# Author: Adhil

from backend.database import db
from sqlalchemy import String, Column, Integer, ForeignKey, Boolean


class Comment(db.Model):
    __tablename__ = "comment"

    id = Column("id", Integer(), primary_key = True)
    article_id = Column("article_id", Integer(), ForeignKey("article.id"))
    hidden = Column("hidden", Boolean(), nullable = False)
    content = Column("content", String(), nullable = False)