from backend.database import db
from backend.utils import create_uuid

from flask_security import RoleMixin


class Role(db.Model, RoleMixin):
	__tablename__ = 'role'
	
	id = db.Column(db.String, primary_key=True, default=create_uuid)

	name = db.Column(db.String, unique=True, nullable=False)
	description = db.Column(db.String)
