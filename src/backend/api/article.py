from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource
from backend.models import *


class ArticlesAPI(Resource):
    
    def post(self):
            article_data = []
            if request.headers.get('Content-Type') == 'application/json':
                article_data = request.get_json()
            else:
                return jsonify('Malformed request!',400)
            new_article = Article(
                                    title = article_data['title'],
                                    content = article_data['content'],
                                    creator = current_user.id,
            )
            try:
                db.session.add(new_article)
                db.session.commit()
                return jsonify('Article created successfully',201)
            except:
                return jsonify('Internal server error',500)
            
    def get(self,article_id=None):
        if not article_id:
            try:
                articles = Article.query.all()
                return jsonify(articles,200)
            except:
                return jsonify('Internal server error',500)
        else:
            try:
                article = Article.query.filter_by(id=article_id).first()
                return jsonify(article,200)
            except:
                return jsonify('Internal server error',500)
            
    def put(self,article_id=None):
        if not article_id:
            return jsonify('Malformed request!',400)
        
        try:
            article = Article.query.filter_by(id=article_id).first()
        except:
            return jsonify('Internal server error',500)
        
        new_article_data = []
        if request.headers.get('Content-Type') == 'application/json':
            new_article_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        
        try:
            article.title = new_article_data['title']
            article.content = new_article_data['content']
            db.session.commit()
            return jsonify('Article modified successfully',200)
        except:
            return jsonify('Malformed request!',400)
        
    def delete(self,article_id=None):
        if not article_id:
            return jsonify('Malformed request!',400)
        
        try:
            article = Article.query.filter_by(id=article_id).first()
            db.session.delete(article)
            db.session.commit()
            return jsonify('Article deleted successfully',200)
        except:
            return jsonify('Internal server error',500)