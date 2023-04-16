from flask_security import login_required
from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import stringify_messages

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
        #sender_id = current_user.id
        ticket_id = args.get('ticket_id',None)

        malformed=[None,'']
        if text in malformed or ticket_id in malformed:
            return {"message":"Malformed request","status":400},400

        TicketExistsCheck=Ticket.query.filter_by(id=ticket_id).first()
        if TicketExistsCheck is None:
                return {"status":404,"message":"Associated ticket not found!"},404

        #Implement MessageExistsCheck upon implementation of Flask_Security
        #MessageExistsCheck=Message.query.filter_by(content=content,article_id=article_id).first()


        new_message = Message(
                                text = text,
                                sender_id = 1,
                                ticket_id = ticket_id,
                                hidden = False,
                                flagged = False
        )
        try:
            db.session.add(new_message)
            db.session.commit()
            return {
                    'status':201,
                    'message':'Message created successfully',
                    'messageID':new_message.id,
                    'text':new_message.text,
                    'senderID':new_message.sender_id,
                    'ticketID':new_message.ticket_id,
                    'posted_at':str(new_message.posted_at),
                    'hidden':new_message.hidden,
                    'flagged':new_message.flagged
            },201
        except:
            return {'message':'Internal server error'},500

    def get(self,message_id=None):
        if message_id:
            args=get_message_parser.parse_args()
            start = args.get('start',0)
            count = args.get('count',None)
            ticket_id = args.get('ticket_id')
            print(start,count,ticket_id)
            
            try:
                ticket = Ticket.query.filter_by(id=ticket_id).first()
                messages = Message.query.filter_by(ticket_id=ticket.id,hidden=False).all()

                if start < 0 or count < 0:
                    return {'message':'Malformed request!'},400
                
                if len(messages) > 10:
                    if start < len(messages) :
                        if count < len(messages):
                            messages = messages[start:start+count+1]
                        else:
                            messages = messages[start:]

                return {
                        'status':200,
                        'message':'Request successful',
                        'ticket_id':ticket.id,
                        'last_response_time':str(ticket.last_response_time),
                        'messages': stringify_messages(messages)
                },200
            except:
                return {'message':'Internal server error'},500
        else:
            return {'message':'No access rights, forbidden!'},403
        
    def delete(self,message_id=None):
        if not message_id:
            return {'message':'Malformed request!'},400
        try:
            message = Message.query.filter_by(id=message_id,hidden=False).first()
            if not message:
                return {'message':'Message doesn\'t exist'},404
            db.session.delete(message)
            db.session.commit()
            return {'message':'Message deleted successfully'},200
        except:
            return {'message':'Internal server error'},500
