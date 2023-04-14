# Author: Afnan, Adhil

from backend.database import db
import uuid

articles_tags = db.Table("articles_tags",
                       db.Column('article_id', db.String, db.ForeignKey('article.id')),
                       db.Column('tag_id', db.String, db.ForeignKey('tag.id'))
                       )