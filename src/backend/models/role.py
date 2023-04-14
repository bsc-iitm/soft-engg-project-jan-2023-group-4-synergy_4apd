# Author: Adhil

from flask_security import RoleMixin
import uuid
from backend.database import db

class Role(db.Model, RoleMixin):
	id = db.Column("id", db.String, primary_key = True, default=str(uuid.uuid4()))
	name = db.Column("name", db.String, unique = True, nullable = False)
	description = db.Column("description", db.String)
