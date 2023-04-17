from backend.database import db


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.String, db.ForeignKey('user.id')),
                       db.Column('role_id', db.String, db.ForeignKey('role.id'))
                       )
