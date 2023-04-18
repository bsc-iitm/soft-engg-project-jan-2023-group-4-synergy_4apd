from flask_security import login_required, auth_required,roles_required
from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import stringify_tickets,stringify_messages,stringify_tags

create_ticket_parser=reqparse.RequestParser()
create_ticket_parser.add_argument('title',required=True,nullable=False)
create_ticket_parser.add_argument('firstMessage',required=True,nullable=False)
create_ticket_parser.add_argument('public',type=bool,required=True,nullable=False)
create_ticket_parser.add_argument('tags',nullable=True)

put_ticket_parser=reqparse.RequestParser()
put_ticket_parser.add_argument('title',nullable=False)
put_ticket_parser.add_argument('public',type=bool,nullable=False,default=False)
put_ticket_parser.add_argument('status',type=int,nullable=False)
put_ticket_parser.add_argument('solution',nullable=False)
put_ticket_parser.add_argument('tags',nullable=False)
put_ticket_parser.add_argument('votes',type=int,nullable=False)
put_ticket_parser.add_argument('assignee',nullable=False)

class TicketAPI(Resource):
    
    # @auth_required("token")
    @login_required
    @roles_required('user')
    def post(self):
        args=create_ticket_parser.parse_args()
        title=args.get('title',None)
        firstMessage=args.get('firstMessage',None)
        public=args.get('public',True)
        tags=args.get('tags',None)

        malformed=[None,'']
        if title in malformed or firstMessage in malformed:
            return {
                    "message":"Malformed request"
            },400
        
        new_ticket = Ticket(
                            title = title,
                            status = 0,
                            votes = 0,
                            is_public = public,
                            creator = current_user.id
        )

        if tags not in malformed:
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if existing_tag:
                    new_ticket.tags.append(existing_tag)

        db.session.add(new_ticket)
        db.session.commit()

        new_firstMessage = Message(
                                text = firstMessage,
                                sender_id = current_user.id,
                                ticket_id = new_ticket.id
        )

        db.session.add(new_firstMessage)
        db.session.commit()

        return {
                "message": "Ticket created successfully",
                "id": new_ticket.id,
                "title": new_ticket.title,
                "status": new_ticket.status,
                "votes": new_ticket.votes,
                "is_public": new_ticket.is_public,
                "creator": new_ticket.creator,
                "assignee": new_ticket.assignee,
                "first_message_id": new_firstMessage.id,
                "first_message_text": new_firstMessage.text,
                'tags': stringify_tags(new_ticket.tags),
                "last_response_time": str(new_ticket.last_response_time)
        },201
    
    @login_required
    @roles_required('user')
    def get(self,ticket_id=None):
        if not ticket_id:
            tickets = Ticket.query.filter_by(is_public=True).all()
            return {
                    'message':'Request Successful',
                    'tickets':stringify_tickets(tickets)
            },200
        
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if not ticket:
            return {
                    "message":"Ticket doesn't exist"
            },404
        
        messages = Message.query.filter_by(ticket_id=ticket_id).all()
        return {
                'id': ticket.id,
                'title': ticket.title,
                'status': ticket.status,
                'votes': ticket.votes,
                "is_public": ticket.is_public,
                "creator": ticket.creator,
                "assignee": ticket.assignee,
                "solution": ticket.solution,
                'last_response_time': str(ticket.last_response_time),
                'messages': stringify_messages(messages),
                'tags': stringify_tags(ticket.tags)
        },200

    @login_required
    @roles_required('user')
    def put(self,ticket_id=None):
        malformed=[None,'']
        if not ticket_id:
            return {
                    'message':'Malformed request!'
            },400
        
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if not ticket:
            return {
                    "message":"Ticket doesn't exist"
            },404
        
        if ticket.creator!=current_user.id and 'support_staff' not in current_user.roles:
            return {"message":"Forbidden!"},403
    
        args=put_ticket_parser.parse_args()
        title=args.get('title',ticket.title)
        public=args.get('public',ticket.is_public)
        status=args.get('status',ticket.status)
        solution=args.get('solution',ticket.solution)
        tags=args.get('tags',None)
        votes=args.get('votes',ticket.votes)
        assignee=args.get('assignee',ticket.assignee)

        if tags not in malformed:
            tags = tags.split(",")
            for tag in tags:
                existing_tag = Tag.query.filter_by(name=tag).first()
                if existing_tag:
                    ticket.tags.append(existing_tag)
        
        ticket.title = title
        ticket.is_public = public
        ticket.status=status
        ticket.solution=solution
        ticket.votes=votes
        ticket.assignee=assignee

        db.session.commit()

        return {
                'message':'Ticket modified successfully',
                'id': ticket.id,
                'title': ticket.title,
                'status': ticket.status,
                'votes': ticket.votes,
                "is_public": ticket.is_public,
                "creator": ticket.creator,
                "assignee": ticket.assignee,
                "solution": ticket.solution,
                'last_response_time': str(ticket.last_response_time),
                'tags': stringify_tags(ticket.tags)
        },200

    @login_required
    @roles_required('user')
    def delete(self,ticket_id=None):
        if not ticket_id:
            return {
                    "message":'Malformed request!'
            },400
        
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        if not ticket:
            return {
                    "message":"Ticket doesn't exist"
            },404
        
        if ticket.creator!=current_user.id and 'support_staff' not in current_user.roles:
            return {"message":"Forbidden!"},403
        
        messages = Message.query.filter_by(ticket_id=ticket_id).all()
        if messages:
            for message in messages:
                db.session.delete(message)
            
        db.session.delete(ticket)
        db.session.commit()
        return {
                'message':'Ticket and associated messages deleted successfully'
        },200

class MyTicketsAPI(Resource):

    @login_required
    @roles_required('user')
    def get(self):
        tickets = Ticket.query.filter_by(creator=current_user.id).all()
        return {
                'message':'Request Successful',
                'tickets':stringify_tickets(tickets)
        },200