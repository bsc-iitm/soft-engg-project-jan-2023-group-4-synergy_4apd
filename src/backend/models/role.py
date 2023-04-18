from backend.database import db
from backend.utils import create_uuid
from flask_security import RoleMixin

class Role(db.Model, RoleMixin):
	__tablename__ = 'role'
	
	id = db.Column(db.String, primary_key=True, default=create_uuid)
	name = db.Column(db.String, unique=True, nullable=False)
	description = db.Column(db.String)


    # user=Role(name="user",description="Default users, mainly students")
    # support_staff=Role(name="support_staff",description="Support Staff")
    # admin=Role(name="admin",description="Administrator")
    # superadmin=Role(name="superadmin",description="Super Administrator")

    # db.session.add(user)
    # db.session.add(support_staff)
    # db.session.add(admin)
    # db.session.add(superadmin)
    # db.session.commit()