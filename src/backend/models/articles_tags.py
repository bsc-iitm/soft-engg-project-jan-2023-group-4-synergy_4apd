# Author: Afnan, Adhil

from backend.database import db

articles_tags = db.Table("articles_tags",
                       db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                       )