# Author: Afnan, Adhil

from backend.database import db
from .articles_tags import *
from backend.utils import createUUID,setTime

class Article(db.Model):
    __tablename__ = "article"
    
    id = db.Column("id", db.String, primary_key = True, default=createUUID)
    title = db.Column("title", db.String, nullable = False)
    created_at = db.Column("created_at", db.DateTime, default = setTime)
    updated_at = db.Column("updated_at", db.DateTime, default = setTime)
    content = db.Column("content", db.String, nullable = False)
    creator = db.Column("creator", db.String, db.ForeignKey("user.id"), nullable = False)

    tags = db.relationship("Tag",secondary=articles_tags,backref=db.backref("article",lazy="dynamic"))
    