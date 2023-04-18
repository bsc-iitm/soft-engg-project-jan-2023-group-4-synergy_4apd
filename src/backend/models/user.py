from backend.database import db
from backend.utils import create_uuid
from flask_security import UserMixin
from sqlalchemy.dialects.sqlite import BLOB

class User(db.Model, UserMixin):
	__tablename__= 'user'
	
	id = db.Column(db.String, primary_key=True, default=create_uuid)
	email = db.Column(db.String, unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	name = db.Column(db.String, nullable=False)
	designation = db.Column(db.String)
	bio = db.Column(db.String)
	phone = db.Column(db.String)
	profile_pic = db.Column(BLOB)
	active = db.Column(db.Boolean, nullable=False)
	fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
	
	roles = db.relationship('Role', secondary='roles_users', backref=db.backref('user', lazy='dynamic'))