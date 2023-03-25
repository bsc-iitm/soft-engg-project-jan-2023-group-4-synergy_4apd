# Author: Adhil

from flask_security import RoleMixin

from backend.database import db
from sqlalchemy import String, Column, Integer

class Role(db.Model, RoleMixin):
	id = Column("id", Integer(), primary_key = True)
	name = Column("name", String(), unique = True, nullable = False)
	description = Column("description", String())