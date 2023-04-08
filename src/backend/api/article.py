from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
from models.article import Article
import uuid

@app.route('/api/v1/admin/articles', methods=['GET','POST'])
@login_required
#@admin -role
def articles():
    if current_user.designation != 'admin':
        return jsonify('No access rights, forbidden!',403)
    
    #POST
    if request.method == 'POST':
        article_data = []
        if request.headers.get('Content-Type') == 'application/json':
            article_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        new_article = Article(
                                id = uuid.uuid4(),
                                title = article_data['title'],
                                content = article_data['content'],
                                creator = current_user.id,
        )
        try:
            db.session.commit()
            return jsonify('Article created successfully',201)
        except:
            return jsonify('Internal server error',500)
        
    #GET
    elif request.method == 'GET':
        articles = Article.query.all()
        return jsonify(articles,200)

    #ERROR
    else:
        return jsonify('Malformed request!',400)
    
@app.route('/api/v1/admin/articles/<string:uuid>', methods=['GET','PUT','DELETE'])
@login_required
def individual_article(uuid):
    if current_user.designation != 'admin':
        return jsonify('No access rights, forbidden!',403)
    
    article = Article.query.filter_by(id=uuid).first()
    
    #GET
    if request.method == 'GET':
        return jsonify(article,200)

    #PUT
    elif request.method == 'PUT':
        new_article_data = []
        if request.headers.get('Content-Type') == 'application/json':
            new_article_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        article.title = new_article_data['title']
        article.content = new_article_data['content']
        try:
            db.session.commit()
            return jsonify('Article updated successfully',201)
        except:
            return jsonify('Internal server error',500)

    #DELETE
    elif request.method == 'DELETE':
        try:
            db.session.delete(article)
            db.session.commit()
            return jsonify('Article deleted successfully',201)
        except:
            return jsonify('Internal server error',500)
        
    #ERROR
    else:
        return jsonify('Malformed request!',400)