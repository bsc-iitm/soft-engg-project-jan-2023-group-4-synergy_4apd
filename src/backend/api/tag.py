from flask_restful import reqparse,Resource
from flask import jsonify
from backend.models import *

create_tag_parser=reqparse.RequestParser()
create_tag_parser.add_argument('name')
create_tag_parser.add_argument('description')

modify_tag_parser=reqparse.RequestParser()
modify_tag_parser.add_argument('tagID')
modify_tag_parser.add_argument('name')
modify_tag_parser.add_argument('description')

get_tag_parser=reqparse.RequestParser()
get_tag_parser.add_argument('tagIDList',location='args')

delete_tag_parser=reqparse.RequestParser()
delete_tag_parser.add_argument('tagID')


class TagAPI(Resource):
    def get(self):
        
        d=get_tag_parser.parse_args()
        ret = d.get('tagIDList')
        
        if ret=='' or ret is None:
            return "Malformed request",400
        
        idl=ret.strip().split(',')
        
        tagIDList,retdict=[],{}

        for i in idl:
            try:
                tagIDList.append(int(i))
            except ValueError:
                tagIDList.append(i)
        
        if tagIDList[0]=="all":
            return "all",200
        else:        
            for i in tagIDList:
                tagi=Tag.query.filter_by(id=i).first()
                if tagi is not None:
                    retdict[tagi.id]=[tagi.id,tagi.name,tagi.description]
                else:
                    return "No matching tags found!",404
        
        return retdict,200

    # def post(self,)
    


    
#print("DONE")