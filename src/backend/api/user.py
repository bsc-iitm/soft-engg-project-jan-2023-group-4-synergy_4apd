from flask_restful import Resource, reqparse
from flask_security import login_required,roles_required
from sqlalchemy.dialects.sqlite import BLOB
from flask_security.utils import hash_password
from flask_login import current_user
from backend.models import *

edit_user_parser=reqparse.RequestParser()
edit_user_parser.add_argument('email')
edit_user_parser.add_argument('password')
edit_user_parser.add_argument('name')
edit_user_parser.add_argument('designation')
edit_user_parser.add_argument('bio')
edit_user_parser.add_argument('phone',type=int)
edit_user_parser.add_argument('profile_pic',type=BLOB)

class UserAPI(Resource):

    @login_required
    @roles_required('user')
    def put(self):
        user = User.query.filter_by(id=current_user.id).first()

        args=edit_user_parser.parse_args()
        email=args.get('email')
        password=args.get('password')
        name=args.get('name')
        designation=args.get('designation')
        bio=args.get('bio')
        phone=args.get('phone')
        profile_pic=args.get('profile_pic')
        
        if User.query.filter_by(email=email).first():
            return {
                    "message":"Email ID already in use"
            },400
        
        user.email = email if email else user.email
        user.name = name if name else user.name
        user.password = hash_password(password) if password else user.password
        user.designation = designation if designation else user.designation
        user.bio = bio if bio else user.bio
        user.phone = phone if phone else user.phone
        user.profile_pic = profile_pic if profile_pic else user.profile_pic  
        
        db.session.commit()
        
        return{
                "message":"User updated successfully",
                "email":user.email,
                "name":user.name,
                "designation":user.designation,
                "bio":user.bio,
                "phone":user.phone,
                "profile_pic":user.profile_pic
        },200
    
    @login_required
    @roles_required('user')
    def get(self):
        user = User.query.filter_by(id=current_user.id).first()
        return{
                "message":"Request successful",
                "email":user.email,
                "name":user.name,
                "designation":user.designation,
                "bio":user.bio,
                "phone":user.phone,
                "profile_pic":user.profile_pic
        },200