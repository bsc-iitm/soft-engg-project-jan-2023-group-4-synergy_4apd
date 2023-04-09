from flask_restful import reqparse,Resource
from backend.models import *

create_tag_parser=reqparse.RequestParser()
create_tag_parser.add_argument('name')
create_tag_parser.add_argument('description')

modify_tag_parser=reqparse.RequestParser()
modify_tag_parser.add_argument('tagID')
modify_tag_parser.add_argument('name')
modify_tag_parser.add_argument('description')

get_tag_parser=reqparse.RequestParser()
get_tag_parser.add_argument('tagIDList')

delete_tag_parser=reqparse.RequestParser()
delete_tag_parser.add_argument('tagID')

class TagAPI(Resource):
    def get(self,tagIDList):
        
        retdict={}
        
        for i in tagIDList:
            tagi=Tag.query.filter_by(id=i).first()
            retdict[tagi.id]=[tagi.id,tagi.name,tagi.description]
        
        return retdict,200
    
    # def post(self,)
    


    
print("DONE")