from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import stringify_articles,stringify_comments,stringify_tags
from datetime import datetime

create_article_parser=reqparse.RequestParser()
create_article_parser.add_argument('title',required=True,nullable=False)
create_article_parser.add_argument('content',required=True,nullable=False)
create_article_parser.add_argument('tags',nullable=True)

put_article_parser=reqparse.RequestParser()
put_article_parser.add_argument('title',required=True,nullable=False)
put_article_parser.add_argument('content',required=True,nullable=False)
put_article_parser.add_argument('tags',nullable=False)


class ArticleAPI(Resource):
    
    def post(self):
        args=create_article_parser.parse_args()

        title=args.get('title',None)
        content=args.get('content',None)
        tags=args.get('tags',None)

        malformed=[None,'']
        if title in malformed or content in malformed:
            return {"message":"Malformed request","status":400},400

        new_article = Article(
                                title = title,
                                content = content,
                                creator = 1,#current_user.id,
        )

        if tags not in malformed:    
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if not existing_tag:
                    try:
                        new_tag = Tag(name=tag)
                        db.session.add(new_tag)
                        db.session.commit()
                    except:
                        return {'message':'Internal server error'},500
                    
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                new_article.tags.append(existing_tag)

        try:
            db.session.add(new_article)
            db.session.commit()
            return {
                    "status" : 201,
                    "article_id" : new_article.id,
                    "message": "Article created successfully",
                    "title" : new_article.title,
                    "content" : new_article.content,
                    "created_at" : str(new_article.created_at),
                    "creator" : new_article.creator,
                    'tags': stringify_tags(new_article.tags),
                    "updated_at" : str(new_article.updated_at)
            },201
        except:
            return {'message':'Internal server error'},500
            
    def get(self,article_id=None):
        if not article_id:
            try:
                articles = Article.query.all()
                return {
                        "status" : 200,
                        "message" : "Request successful",
                        "articles" : stringify_articles(articles)
                },200
            except:
                return {'message':'Internal server error'},500
        else:
            try:
                article = Article.query.filter_by(id=article_id).first()
                if not article:
                    return {"message":"Article doesn't exist"},404
                comments = Comment.query.filter_by(article_id=article.id).all()
                return {
                        "article_id" : article.id,
                        "title" : article.title,
                        "content" : article.content,
                        "creator" : article.creator,
                        "created_at" : str(article.created_at),
                        "updated_at" : str(article.updated_at),
                        "comments": stringify_comments(comments),
                        "tags": stringify_tags(article.tags)
                },200
            except:
                return {'message':'Internal server error'},500
            
    def put(self,article_id=None):

        malformed=[None,'']
        if article_id in malformed:
            return {'message':'Malformed request!'},400
        
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {"message":"Article doesn't exist"},404
        
        args = put_article_parser.parse_args()
            
        title = args.get('title',article.title)
        content = args.get('content',article.content)
        tags = args.get('tags',None)

        
        if title in malformed or content in malformed:
            return {'message':'Malformed request!'},400
        
        article.title = title
        article.content = content
        article.updated_at = datetime.now()
      
        
        if tags not in malformed:
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if not existing_tag:
                    try:
                        new_tag = Tag(name=tag)
                        db.session.add(new_tag)
                        db.session.commit()
                    except:
                        return {'message':'Internal server error'},500
            
            article.tags=[]
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                article.tags.append(existing_tag)
        
        if tags=="":
            article.tags=[]

        db.session.commit()

        article = Article.query.filter_by(id=article_id).all()
        return {'message':'Article modified successfully',"article":stringify_articles(article)},200

        
    def delete(self,article_id=None):
        if not article_id:
            return {'message':'Malformed request!'},400
        
        try:
            article = Article.query.filter_by(id=article_id).first()
            if not article:
                return {"message":"Article doesn't exist"},404
            db.session.delete(article)
            db.session.commit()
            return {'message':'Article deleted successfully'},200
        except:
            return {'message':'Internal server error'},500