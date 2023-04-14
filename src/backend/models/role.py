# Author: Adhil

from flask_security import RoleMixin
from backend.utils import createUUID
from backend.database import db

class Role(db.Model, RoleMixin):
	id = db.Column("id", db.String, primary_key = True, default=createUUID)
	name = db.Column("name", db.String, unique = True, nullable = False)
	description = db.Column("description", db.String)
