from flask import request

from flask import request, jsonify
from flask_security import Security, SQLAlchemyUserDatastore,login_required
from flask_security.utils import hash_password
from flask_login import current_user
from models.user import User
import uuid

user_datastore = SQLAlchemyUserDatastore(db,User,Role)
security = Security(app,user_datastore)
  
@app.route('/api/v1/user', methods=['GET','POST','PUT','DELETE'])
@login_required
def user():
    #POST
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
           user_data = request.get_json()
        else:
            return 'Content-Type not supported!'
        user_datastore.create_user(
                                    id = uuid.uuid4()
                                    name = user_data['name'],
                                    email = user_data['email'],
                                    password = hash_password(user_data['password']),
                                    pic = user_data['pic'],
                                    bio = user_data['bio'],
                                    phone = user_data['phone'],
                                    designation = user_data['designation']
        )
        try:
            db.session.commit()
            return jsonify('User created successfully',201)
        except:
            return jsonify('Internal server error',500)
    
    #GET
    elif request.method == 'GET':
        return jsonify({
                        'name' : current_user.name,
                        'email' : current_user.email,
                        'pic' : current_user.pic,
                        'bio' : current_user.bio,
                        'phone' : current_user.phone,
                        'designation' : current_user.designation
        },200)
    
    #PUT
    elif request.method == 'PUT':
        if request.headers.get('Content-Type') == 'application/json':
           new_user_data = request.get_json()
        else:
            return 'Content-Type not supported!'
        current_user = (
                        name = new_user_data['name'],
                        email = new_user_data['email'],
                        password = hash_password(new_user_data['password']),
                        pic = new_user_data['pic'],
                        bio = new_user_data['bio'],
                        phone = new_user_data['phone'],
                        designation = new_user_data['designation']
        )
        try:
            db.session.commit()
            return jsonify('User updated successfully',200)
        except:
            return jsonify('Internal server error',500)
        
    #DELETE
    elif  request.method == 'DELETE':
        try:
            current_user.delete()
            db.session.commit()
            return jsonify('User deleted successfully',200)
        except:
            return jsonify('Internal server error',500)
    
    #ERROR
    else:
        return jsonify('No access rights, forbidden!',403)
    
@app.route('/api/v1/admin/user', methods=['POST','DELETE'])
@login_required
def admin():
    #POST
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
           user_data = request.get_json()
        else:
            return 'Content-Type not supported!'
        if user_data['action'] == 'promote':
            try:
                pass
            except:
                return jsonify('Malformed request',400)
        elif user_data['action'] == 'demote':
            try:
                pass
            except:
                return jsonify('Malformed request',400)
        else:
            return jsonify('No access rights; Forbidden',403)
        
    #DELETE
    elif request.method == 'DELETE':
        pass

    #ERROR
    else:
        return jsonify('No access rights, forbidden!',403)