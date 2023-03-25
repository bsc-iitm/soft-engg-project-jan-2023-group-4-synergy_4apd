# Author: Preetodeep, Afnan
from backend.database import db

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(128), nullable=True)
