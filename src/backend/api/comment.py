from flask_login import current_user
from flask_restful import reqparse,Resource
from flask_security import login_required,roles_required
from backend.models import *
from datetime import datetime
from backend.utils import stringify_comments

create_comment_parser=reqparse.RequestParser()
create_comment_parser.add_argument('articleUUID',required=True)
create_comment_parser.add_argument('content',required=True)
create_comment_parser.add_argument('hidden',type=bool,default=False,nullable=False)

get_comment_parser=reqparse.RequestParser()
get_comment_parser.add_argument('articleUUID',location='args',required=True)


class CommentAPI(Resource):
    @login_required
    @roles_required('user')
    def get(self):
        args=get_comment_parser.parse_args()
        article_id=args.get('articleUUID',None)

        malformed=[None,'']
        if article_id in malformed:
            return {
                    "message":"Malformed request"
            },400

        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {
                    "message":"Article doesn't exist!"
            },404

        comments = Comment.query.filter_by(article_id=article_id, hidden=False).all()

        return {
                "message":"Request successful",
                "article_id":article_id,
                "comments":stringify_comments(comments)
        },200

    @login_required
    @roles_required('support_staff')
    def post(self):
        args=create_comment_parser.parse_args()
        article_id=args.get('articleUUID',None)
        content=args.get('content',None)
        hidden=args.get('hidden',False)
        
        malformed=[None,'']
        if article_id in malformed or content in malformed:
            return {
                    "message":"Malformed request"
            },400
        
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {
                    "message":"Article doesn't exist!"
            },404
        
        existing_comment = Comment.query.filter_by(content=content,article_id=article_id).first()
        if not existing_comment:
            return {
                    "message":"Comment already exists!"
            },400

        new_comment = Comment(
                                article_id=article_id,
                                content=content,
                                hidden=hidden
        )

        db.session.add(new_comment)
        article.updated_at=datetime.now()
        db.session.commit()

        return {
                "message":"Request successful",
                "id":new_comment.id,
                "content":new_comment.content,
                "posted_at":str(new_comment.posted_at),
                "article_id":new_comment.article_id,
                "hidden":new_comment.hidden
        },201
                
        
    @login_required
    @roles_required('support_staff')
    def delete(self,comment_id=None):
        if not comment_id:
            return {
                    "message":"Malformed request"
            },400
        
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            return {
                    "message":"Comment doesn't exist!"
            },404
    
        db.session.delete(comment)
        db.session.commit()
        return {
                "message":"Deletion successful!"
        },200