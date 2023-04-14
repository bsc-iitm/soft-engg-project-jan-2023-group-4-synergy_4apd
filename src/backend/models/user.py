# Author: Adhil

from backend.database import db

from sqlalchemy.dialects.sqlite import BLOB
from flask_security import UserMixin
import uuid
from .roles_users import *

class User(db.Model,UserMixin):
	
	__tablename__="user"
	
	id = db.Column("id", db.String, primary_key = True, default=str(uuid.uuid4()))
	name = db.Column("name", db.String,nullable = False)
	email = db.Column("email", db.String, unique = True, nullable = False)
	password_hash = db.Column("password_hash", db.String, nullable=False)
	profile_pic = db.Column("profile_pic", BLOB)
	bio = db.Column("bio", db.String)
	phone = db.Column("phone", db.Integer)
	designation = db.Column("designation", db.String, nullable = False)
	
	active = db.Column("active", db.Boolean)
	fs_uniquifier = db.Column("fs_uniquifier", db.String(255), unique = True, nullable = False)
	
	roles = db.relationship("Role", secondary=roles_users, backref=db.backref("user", lazy="dynamic"))
