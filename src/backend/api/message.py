from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
import uuid
from flask_restful import Resource
from backend.models import *   

class MessageAPI(Resource):
    def post(self):
        message_data = []
        if request.headers.get('Content-Type') == 'application/json':
            message_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        
        text = message_data['text']
        sender_id = current_user.id
        ticket_id = message_data['ticket_id']
        new_message = Message(
                                text = text,
                                sender_id = sender_id,
                                ticket_id = ticket_id,
                                hidden = False,
                                flagged = False
        )
        try:
            db.session.add(new_message)
            db.session.commit()
            return jsonify('Message created successfully',201)
        except:
            return jsonify('Internal server error',500)

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
