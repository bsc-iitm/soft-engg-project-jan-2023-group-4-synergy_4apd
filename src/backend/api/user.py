from flask_restful import Resource, reqparse
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

    def put(self):
        user = User.query.filter_by(id=current_user.id).first()
        args=edit_user_parser.parse_args()
        email=args.get('email',user.email)
        password=args.get('password',None)
        name=args.get('name',user.name)
        designation=args.get('designation',user.designation)
        bio=args.get('bio',user.bio)
        phone=args.get('phone',user.phone)
        profile_pic=args.get('profile_pic',user.profile_pic)

        if User.query.filter_by(email=email).first():
            return {
                    "message":"Email ID already in use"
            },400
        
        user.email = email
        if password:
            user.password = hash_password(password)
        user.name = name
        user.designation = designation
        user.bio = bio
        user.phone = phone
        user.profile_pic = profile_pic

        
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
