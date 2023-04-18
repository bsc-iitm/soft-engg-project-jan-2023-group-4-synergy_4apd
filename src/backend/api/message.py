from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import stringify_messages
from datetime import datetime

create_message_parser=reqparse.RequestParser()
create_message_parser.add_argument('text',required=True,nullable=False)
create_message_parser.add_argument('ticket_id',required=True,nullable=False)

get_message_parser=reqparse.RequestParser()
get_message_parser.add_argument('start',location='args',type=int,required=True,nullable=False)
get_message_parser.add_argument('count',location='args',type=int,required=True,nullable=False)
get_message_parser.add_argument('ticket_id',location='args',required=True,nullable=False)

class MessageAPI(Resource):
    def post(self):
        args=create_message_parser.parse_args()
        text = args.get('text',None)
        ticket_id = args.get('ticket_id',None)

        malformed=[None,'']
        if text in malformed or ticket_id in malformed:
            return {
                    "message":"Malformed request"
            },400

        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if not ticket:
            return {
                    "message":"Associated ticket not found!"
            },404

        existing_message = Message.query.filter_by(text=text,ticket_id=ticket.id,sender_id=current_user.id).first()
        if existing_message:
            return {
                    "message":"Message already exists!"
            },400

        new_message = Message(
                                text = text,
                                sender_id = current_user.id,
                                ticket_id = ticket_id,
                                hidden = False,
                                flagged = False
        )

        db.session.add(new_message)
        ticket.last_response_time=datetime.now()
        db.session.commit()

        return {
                'message':'Message created successfully',
                'id':new_message.id,
                'text':new_message.text,
                'posted_at':str(new_message.posted_at),
                'sender_id':new_message.sender_id,
                'ticket_id':new_message.ticket_id,
                'hidden':new_message.hidden,
                'flagged':new_message.flagged
        },201

    def get(self):
        args=get_message_parser.parse_args()
        start = args.get('start',0)
        count = args.get('count',0)
        ticket_id = args.get('ticket_id')
        
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        print(ticket)
        if not ticket:
            return {
                    "message":"Associated ticket not found!"
            },404
    
        messages = Message.query.filter_by(ticket_id=ticket.id,hidden=False).all()
        print(messages)

        if start < 0 or count < 0:
            return {
                    'message':'Malformed request!'
            },400
        
        if len(messages) > 10:
            if start < len(messages): 
                if count < len(messages):
                    messages = messages[start:start+count]
                else:
                    messages = messages[start:]

        return {
                'message':'Request successful',
                'ticket_id':ticket.id,
                'last_response_time':str(ticket.last_response_time),
                'messages': stringify_messages(messages)
        },200
        
    def delete(self,message_id=None):
        if not message_id:
            return {
                    'message':'Malformed request!'
            },400

        message = Message.query.filter_by(id=message_id,hidden=False).first()
        if not message:
            return {
                    "message":"Message doesn't exist"
            },404
        
        db.session.delete(message)
        db.session.commit()
        return {
                'message':'Message deleted successfully'
        },200
