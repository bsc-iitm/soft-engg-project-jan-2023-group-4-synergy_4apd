# Author: Preetodeep, Afnan
from backend.database import db

from sqlalchemy import Column, Integer, String

class Tag(db.Model):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(128), nullable=True)
