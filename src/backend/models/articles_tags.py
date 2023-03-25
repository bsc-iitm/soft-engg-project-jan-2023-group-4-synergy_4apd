# Author: Afnan, Adhil

from sqlalchemy import Table, Column, Integer, ForeignKey

articles_tags = Table("articles_tags",
                       Column('article_id', Integer, ForeignKey('article.id')),
                       Column('tag_id', Integer, ForeignKey('tag.id'))
                       )