from flask_restful import reqparse,Resource
from flask_security import roles_required,login_required
from backend.models import *
from backend.utils import stringify_tags

create_tag_parser=reqparse.RequestParser()
create_tag_parser.add_argument('name',required=True)
create_tag_parser.add_argument('description')       

modify_tag_parser=reqparse.RequestParser()
modify_tag_parser.add_argument('tagID')
modify_tag_parser.add_argument('name')
modify_tag_parser.add_argument('description')

get_tag_parser=reqparse.RequestParser()
get_tag_parser.add_argument('name',location='args',required=True)
get_tag_parser.add_argument('tagIDList',location='args',required=True)

class TagAPI(Resource):

    @login_required
    @roles_required('user')
    def get(self):
        args=get_tag_parser.parse_args()
        name = args.get('name',None)
        tagIDList = args.get('tagIDList',None)

        if tagIDList=="all":
            tags = Tag.query.all()
            return {
                "message":"Request successful",
                "tags":stringify_tags(tags)
            },200
        
        elif name:
            tags = Tag.query.filter_by(name=name).all()
            return {
                    "message":"Request successful",
                    "tags":stringify_tags(tags)
            },200
                        
        elif tagIDList:
            tagIDList = tagIDList.split(",")
            tagList = [Tag.query.filter_by(id=tagID).first() for tagID in tagIDList]
            print(tagList)
            return {
                "message":"Request successful",
                "tags":stringify_tags(tagList)
            },200
        
        else:
            return {
                    "message":"Malformed request!"
            },400
        
    @login_required
    @roles_required('support_staff')
    def post(self):
        args=create_tag_parser.parse_args()
        name = args.get('name',None)
        description = args.get('description',"")

        if name == '':
            return {
                    "message":"Malformed request!"
            },400

        existing_tag = Tag.query.filter_by(name=name).first()
        if existing_tag:
            return {
                    "message":"Tag already exists!"
            },200
        
        new_tag = Tag(
                        name=name,
                        description=description
        )

        db.session.add(new_tag)
        db.session.commit()

        return {
                "message":"Request successful",
                "id":new_tag.id,
                "name":new_tag.name,
                "description":new_tag.description
        },201

    @login_required
    @roles_required('support_staff')
    def delete(self,tag_id=None):
        if not tag_id:
            return {
                    "message":"Malformed request!"
            },400

        tag = Tag.query.filter_by(id=tag_id).first()

        if not tag:
            return {
                    "message":"Tag doesn't exist!"
            },404
        
        db.session.delete(tag)
        db.session.commit()
        return {
                "message":"Tag successfully deleted"
        },200          