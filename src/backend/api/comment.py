from flask_login import current_user
from flask_restful import reqparse,Resource
from flask import jsonify
from backend.models import *


create_comment_parser=reqparse.RequestParser()
create_comment_parser.add_argument('articleUUID',required=True)
create_comment_parser.add_argument('content',required=True)
create_comment_parser.add_argument('hidden',type=bool,default=False,nullable=False)

get_comment_parser=reqparse.RequestParser()
get_comment_parser.add_argument('articleUUID',location='args',required=True)


class CommentAPI(Resource):
    def get(self):

        args=get_comment_parser.parse_args()
        articleUUID=args.get('articleUUID',None)

        malformed=[None,'']
        if articleUUID in malformed:
            return {"message":"Malformed request","status":400},400

        else:
            
            articleCheck=Article.query.filter_by(id=articleUUID).first()
            if articleCheck is None:
                return {"status":404,"message":"Article doesn't exist!"},404

            comment=Comment.query.filter_by(article_id=articleUUID,hidden=False).all()

            if len(comment) == 0:
                return {"message":"No comments for the article","status":200},200
            
            else:
                comments=[]
                for i in comment:
                    commentreturn={}
                    commentreturn['id']=i.id
                    commentreturn['content']=i.content
                    comments.append(commentreturn)

                return {"status":200,"message":"Request successful","articleID":articleUUID,"comments":comments},200


    def post(self):
        args=create_comment_parser.parse_args()
        article_id=args.get('articleUUID',None)
        content=args.get('content',None)
        hidden=args.get('hidden',False)
        
        malformed=[None,'']
        if article_id in malformed or content in malformed:
            return {"message":"Malformed request","status":400},400
        
        ArticleExistsCheck=Article.query.filter_by(id=article_id).first()
        CommentExistsCheck=Comment.query.filter_by(content=content,article_id=article_id).first()

        if ArticleExistsCheck is not None and CommentExistsCheck is None:
            newComment=Comment(article_id=article_id,content=content,hidden=hidden)
            db.session.add(newComment)
            db.session.commit()
            return {"status":201,"message":"Request successful",
                    "articleID":article_id,
                    "commentID":newComment.id,
                    "content":newComment.content},201
        else:
            if ArticleExistsCheck is None:
                return {"status":404,"message":"Article doesn't exist!"},404
            if CommentExistsCheck is not None:
                return {"status":400,"message":"Comment already exists!"},400
        

    def delete(self,comment_UUID=None):

        malformed=[None]
        if comment_UUID in malformed:
            return {"message":"Malformed request","status":400},400
        
        x=Comment.query.filter_by(id=comment_UUID).first()

        if x==None:
            return {"status":404,"message":"Comment doesn't exist!"},404
        else:
            db.session.delete(x)
            db.session.commit()
            return {"status":200,"message":"Deletion successful!"},200