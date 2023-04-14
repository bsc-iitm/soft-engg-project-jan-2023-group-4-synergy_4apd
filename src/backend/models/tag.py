# Author: Preetodeep, Afnan
from backend.database import db
import uuid

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.String, primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(128), nullable=True)
