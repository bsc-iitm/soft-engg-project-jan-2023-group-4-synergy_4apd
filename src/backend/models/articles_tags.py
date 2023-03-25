# Author: Afnan, Adhil

from backend.database import db

from sqlalchemy import Column, Integer, ForeignKey


class ArticlesTags(db.Model):
    __tablename__ = 'articles_tags'

    id = Column(Integer, primary_key=True)
    article_id = Column('article_id', Integer, ForeignKey('article.id'))
    tag_id = Column('tag_id', Integer, ForeignKey('tag.id'))