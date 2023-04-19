from flask_restful import Resource, reqparse
from flask_security import login_required,roles_required
from flask_security.utils import hash_password
from flask_login import current_user
from backend.models import *
from backend.utils import *

edit_user_parser=reqparse.RequestParser()
edit_user_parser.add_argument('action',required=True,nullable=False)

class RoleAPI(Resource):

    @roles_required("admin")
    def put(self,user_id):

        args=edit_user_parser.parse_args()
        action=args.get('action',None)

        user=User.query.filter_by(id=user_id).first()
        if not user:
            return {
                    "message":"Malformed request"
            },400

        if action not in ['promote','demote']:
            return {
                    "message":"Malformed request"
            },400
        

        if 'superadmin' not in current_user.roles:
            if 'admin' in user.roles or action=='demote':
                return {
                    "message":"Forbidden!"
                },403
            if 'support_staff' in user.roles and action=='promote':
                return {
                    "message":"Forbidden!"
                },403

            newRole=Role.query.filter_by(name="support_staff").first()
            user.roles.append(newRole)
            db.session.commit()
            return {
                    "message":"User promoted successfully to support staff!"
            },200
        
                # if 'support_staff' not in user.roles:
                #     return {
                #     "message":"User already at lowest role hierarchy!"
                #     },400
                
                # else:
        
        else:
            if action=='demote':
                if 'superadmin' in user.roles:
                    oldRole=Role.query.filter_by(name="superadmin").first()
                    user.roles.remove(oldRole)
                    db.session.commit()
                    return {
                            "message":"Super Administrator demoted successfully to admin!"
                    },200
                
                if 'admin' in user.roles:
                    oldRole=Role.query.filter_by(name="admin").first()
                    user.roles.remove(oldRole)
                    db.session.commit()
                    return {
                            "message":"Administrator demoted successfully to support staff!"
                    },200

                if 'support_staff' in user.roles:
                    oldRole=Role.query.filter_by(name="support_staff").first()
                    user.roles.remove(oldRole)
                    db.session.commit()
                    return {
                            "message":"Support staff demoted successfully to user!"
                    },200
                
                return {
                        "message":"User already at lowest role hierarchy!"
                },400
            
            elif action=='promote':
                if 'superadmin' in user.roles:
                    return {
                            "message":"User already at highest role hierarchy!"
                    },400
                
                if 'admin' in user.roles:
                    newRole=Role.query.filter_by(name="superadmin").first()
                    user.roles.append(newRole)
                    db.session.commit()
                    return {
                            "message":"Administrator promoted successfully to Super Administrator!"
                    },200

                if 'support_staff' in user.roles:
                    newRole=Role.query.filter_by(name="admin").first()
                    user.roles.append(newRole)
                    db.session.commit()
                    return {
                            "message":"Support staff promoted successfully to administrator!"
                    },200
                
                newRole=Role.query.filter_by(name="support_staff").first()
                user.roles.append(newRole)
                db.session.commit()
                return {
                        "message":"User promoted successfully to support staff!"
                },200











