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
get_tag_parser.add_argument('tagIDList',location='args')
get_tag_parser.add_argument('name',location='args')


class TagAPI(Resource):
    def get(self):
        
        d=get_tag_parser.parse_args()
        ret = d.get('tagIDList',None)
        retname = d.get('name',None)
        if (ret=='' or ret is None) and (retname=='' or retname is None):
            return {"status":400,"message":"Malformed request!"},400
        
        if retname is not None and retname != '':
            namelist,retdict=[],[]
            for i in retname.strip().split(','):
                    namelist.append(i)
            missing=False
            for i in namelist:
                tagn=Tag.query.filter_by(name=i).first()
                if tagn is not None:
                    retdict.append({"tagID":tagn.id,"name":tagn.name,"description":tagn.description})
                else:
                    missing=True
                    continue

            if missing and len(retdict)==0:
                return {"status":404,"message":"No matching tags found!"},404
            
            return {"status":200,"message":"Request successful","tags":retdict},200

        if ret is not None:
            idl=ret.strip().split(',')
            tagIDList,retdict=[],[]

            for i in idl:
                try:
                    tagIDList.append(int(i))
                except ValueError:
                    tagIDList.append(i)
            print(tagIDList)
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

        if x is None:
        
            dbObj=Tag(name=tagName,description=tagDescription)
            db.session.add(dbObj)
            db.session.commit()

            return {"status":201,"message":"Request successful","tagID":dbObj.id,"tagName":dbObj.name,"tagDescription":dbObj.description},201
        else:
            return {"status":200,"message":"Tag already exists!"},200
    

    def delete(self,tag_id=None):

        if tag_id=='' or tag_id is None:
            return {"status":400,"message":"Malformed request!"},400

        x=Tag.query.filter_by(id=tag_id).first()

        if x==None:
            return {"status":404,"message":"Tag doesn't exist!"},404
        else:
            db.session.delete(x)
            db.session.commit()
            return {"status":200,"message":"Deletion successful!"},200
        
            