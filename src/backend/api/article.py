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
            return {
                    "message":"Malformed request"
            },400

        new_article = Article(
                                title = title,
                                content = content,
                                creator = current_user.id,
        )

        if tags not in malformed:    
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if not existing_tag:
                    new_tag = Tag(name=tag)
                    db.session.add(new_tag)
                    new_article.tags.append(new_tag)
                else:
                    new_article.tags.append(existing_tag)                

        db.session.add(new_article)
        db.session.commit()

        return {
                "message": "Article created successfully",
                "id" : new_article.id,
                "creator" : new_article.creator,
                "title" : new_article.title,
                "content" : new_article.content,
                "created_at" : str(new_article.created_at),
                "updated_at" : str(new_article.updated_at),
                "tags" : stringify_tags(new_article.tags)
        },201
            
    def get(self,article_id=None):
        if not article_id:
            articles = Article.query.all()
            return {
                    "message" : "Request successful",
                    "articles" : stringify_articles(articles)
            },200
        
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {
                    "message":"Article doesn't exist"
            },404
        
        comments = Comment.query.filter_by(article_id=article.id).all()
        return {
                "id" : article.id,
                "creator" : article.creator,
                "title" : article.title,
                "content" : article.content,
                "created_at" : str(article.created_at),
                "updated_at" : str(article.updated_at),
                "comments": stringify_comments(comments),
                "tags": stringify_tags(article.tags)
        },200
            
    def put(self,article_id=None):
        malformed=[None,'']
        if article_id in malformed:
            return {
                    'message':'Malformed request!'
            },400
        
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {
                    "message":"Article doesn't exist"
            },404
        
        args = put_article_parser.parse_args() 
        title = args.get('title',article.title)
        content = args.get('content',article.content)
        tags = args.get('tags',None)
        
        if title in malformed or content in malformed:
            return {
                    'message':'Malformed request!'
            },400
        
        article.title = title
        article.content = content
        article.updated_at = datetime.now()
        
        if tags not in malformed:
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if not existing_tag:
                    new_tag = Tag(name=tag)
                    db.session.add(new_tag)
                    article.tags.append(new_tag)
                else:
                    article.tags.append(existing_tag)

        db.session.commit()

        return {
                "message": "Article modified successfully",
                "id" : article.id,
                "creator" : article.creator,
                "title" : article.title,
                "content" : article.content,
                "created_at" : str(article.created_at),
                "updated_at" : str(article.updated_at),
                "tags" : stringify_tags(article.tags)
        },200
        
    def delete(self,article_id=None):
        if not article_id:
            return {
                    'message':'Malformed request!'
            },400
        
        article = Article.query.filter_by(id=article_id).first()
        if not article:
            return {
                    "message":"Article doesn't exist"
            },404
        
        db.session.delete(article)
        db.session.commit()
        
        return {
                'message':'Article deleted successfully'
        },200