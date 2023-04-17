from backend.database import db
from backend.utils import create_uuid


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.String, primary_key=True, default=create_uuid)

    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(128), nullable=True)
