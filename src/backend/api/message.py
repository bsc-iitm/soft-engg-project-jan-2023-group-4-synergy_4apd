from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
import uuid
from flask_restful import Resource
from backend.models import *   

class MessageAPI(Resource):
    def get(self,message_id=None):
        if not message_id:
            start = request.args.get('start')
            count = request.args.get('count')
            ticket_id = request.args.get('ticket_id')
            try:
                messages = Message.query.filter_by(ticket_id=ticket_id,hidden=False).all()
                return jsonify(messages,200)
            except:
                return jsonify('Internal server error',500)
        else:
            return jsonify('No access rights, forbidden!',403)
        
    def delete(self,message_id=None):
        if message_id:
            message = Message.query.filter_by(id=message_id,hidden=False).first()
            try:
                db.session.delete(message)
                db.session.commit()
            except:
                return jsonify('Internal server error',500)
        else:
            return jsonify('Malformed Request',403)
