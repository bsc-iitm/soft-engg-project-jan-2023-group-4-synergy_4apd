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
        ret = d.get('tagIDList',None)
        
        if ret=='' or ret is None:
            return {"status":400,"message":"Malformed request!"},400
        
        idl=ret.strip().split(',')
        
        tagIDList,retdict=[],[]

        for i in idl:
            try:
                tagIDList.append(int(i))
            except ValueError:
                tagIDList.append(i)
        
        if tagIDList[0]=="all":
            tagi=Tag.query.all()
            for i in tagi:
                retdict.append({"tagID":i.id,"name":i.name,"description":i.description})
            return {"status":200,"message":"Request successful","tags":retdict},200
        else:
            missing=False        
            for i in tagIDList:
                tagi=Tag.query.filter_by(id=i).first()
                if tagi is not None:
                    retdict.append({"tagID":tagi.id,"name":tagi.name,"description":tagi.description})
                else:
                    missing=True
                    continue

        if missing and len(retdict)==0:
            return {"status":404,"message":"No matching tags found!"},404
        
        return {"status":200,"message":"Request successful","tags":retdict},200

    def post(self):
        d=create_tag_parser.parse_args()
        tagName,tagDescription=d.get('name',None),d.get('description',None)

        if tagName=='' or tagName is None:
            return {"status":400,"message":"Malformed request!"},400

        x=Tag.query.filter_by(name=tagName).first()

        if tagName != x.name:
        
            dbObj=Tag(name=tagName,description=tagDescription)
            db.session.add(dbObj)
            db.session.commit()

            return {"status":201,"message":"Request successful"},201
        else:
            return {"status":200,"message":"Tag already exists!"},200



    
#print("DONE")