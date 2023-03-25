# Author: Adhil

from flask_security import RoleMixin

from backend.database import db

class Role(db.Model, RoleMixin):
	id = db.Column("id", db.Integer, primary_key = True)
	name = db.Column("name", db.String, unique = True, nullable = False)
	description = db.Column("description", db.String)
