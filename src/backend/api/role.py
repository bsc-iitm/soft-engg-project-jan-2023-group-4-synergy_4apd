from flask_restful import Resource, reqparse
from flask_security import login_required,roles_required
from flask_security.utils import hash_password
from flask_login import current_user
from backend.models import *

edit_user_parser=reqparse.RequestParser()
#edit_user_parser.add_argument('user_id')
edit_user_parser.add_argument('action')

class RoleAPI(Resource):

    @login_required
    @roles_required("admin")
    def put(self,user_id=None):
        if not user_id or user_id=="":
            return {
                    "message":"Malformed request"
            },400

