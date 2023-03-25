# Author: Adhil

from backend.database import db
from sqlalchemy import Column, Integer, String, Boolean

from sqlalchemy.dialects.sqlite import BLOB
from flask_security import UserMixin

from .roles_users import *

class User(db.Model,UserMixin):
	
	__tablename__="user"
	
	id = Column("id", Integer(), primary_key = True)
	name = Column("name", String(),nullable = False)
	email = Column("email", String(), unique = True, nullable = False)
	password_hash = Column("password_hash", String(), nullable=False)
	profile_pic = Column("profile_pic", BLOB)
	bio = Column("bio", String())
	phone = Column("phone", Integer())
	designation = Column("designation", String(), nullable = False)
	
	active = Column("active", Boolean(), nullable = False)
	fs_uniquifier = Column("fs_uniquifier", String(255), unique = True, nullable = False)
	
	roles = db.relationship("Role",secondary=roles_users,backref=db.backref("user",lazy="dynamic"))
