# Author: Afnan, Adhil

from backend.database import db
from datetime import datetime

from .articles_tags import *
import uuid

class Article(db.Model):
    __tablename__ = "article"
    
    id = db.Column("id", db.String, primary_key = True, default=str(uuid.uuid4()))
    title = db.Column("title", db.String, nullable = False)
    created_at = db.Column("created_at", db.DateTime, default = datetime.now())
    updated_at = db.Column("updated_at", db.DateTime, default = datetime.now())
    content = db.Column("content", db.String, nullable = False)
    creator = db.Column("creator", db.String, db.ForeignKey("user.id"), nullable = False)

    tags = db.relationship("Tag",secondary=articles_tags,backref=db.backref("article",lazy="dynamic"))
    