# Author: Afnan, Adhil

from backend.database import db
from sqlalchemy import String, Column, Integer, DateTime, ForeignKey
from datetime import datetime

from .articles_tags import *

class Article(db.Model):
    __tablename__ = "article"
    
    id = Column("id", Integer(), primary_key = True)
    title = Column("title", String(), nullable = False)
    created_at = Column("created_at", DateTime(), default = datetime.now())
    updated_at = Column("updated_at", DateTime(), default = datetime.now())
    content = Column("content", String(), nullable = False)
    creator = Column("creator", Integer(), ForeignKey("user.id"), nullable = False)

    tags = db.relationship("Tag",secondary=articles_tags,backref=db.backref("article",lazy="dynamic"))
    