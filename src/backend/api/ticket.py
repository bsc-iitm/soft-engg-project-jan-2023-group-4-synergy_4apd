from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
import uuid
from flask_restful import Resource
from backend.models import *    

class TicketsAPI(Resource):
    
    def post(self):
        ticket_data = []
        if request.headers.get('Content-Type') == 'application/json':
            ticket_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        
        new_ticket = Ticket(
                            id = uuid.uuid4(),
                            title = ticket_data['title'],
                            status = 'status',
                            votes = 0,
                            is_public = True,
                            creator = current_user.id,
                            assignee = 'user_id',
                            solution = 'message_id',
                            last_response_time = 'NIL',
                            tags = '1,2,3,',
        )
        try:
            db.session.add(new_ticket)
            db.session.commit()
            return jsonify('Ticket created successfully',201)
        except:
            return jsonify('Internal server error',500)
        
            
    def get(self,ticket_id=None):
        if not ticket_id:
            try:
                tickets = Ticket.query.filter_by(is_public=True).all()
                return jsonify(tickets, 200)
            except:
                return jsonify('Internal server error',500)
        else:
            try:
                ticket = Ticket.query.filter_by(id=ticket_id).first()
                messages = Message.query.filter_by(ticket_id=ticket_id).all()
                return jsonify({
                                'ticketID': ticket.id,
                                'votes': ticket.votes,
                                'title': ticket.title,
                                'status': ticket.status,
                                'solutionID': ticket.solution,
                                'last_response_time': ticket.last_response_time,
                                'messages': messages
                },200)
            except:
                return jsonify('Internal server error',500)

    def put(self,ticket_id):
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        new_ticket_data = []
        if request.headers.get('Content-Type') == 'application/json':
            new_ticket_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        
        try:
            ticket.title = new_ticket_data['title']
            ticket.is_public = True if new_ticket_data['visibility'] == 'public' else False
            db.session.commit()
            return jsonify('Ticket modified successfully',200)
        except:
            return jsonify('Malformed request!',400)
        
    def delete(self,ticket_id):
        ticket = Ticket.query.filter_by(id=ticket_id).first()
        try:
            db.session.delete(ticket)
            db.session.commit()
            return jsonify('Ticket deleted successfully',200)
        except:
            return jsonify('Internal server error',500)
        

class MyTicketsAPI(Resource):
    def get(self):
        try:
            tickets = Ticket.query.filter_by(creator=current_user.id).all()
            return jsonify(tickets, 200)
        except:
            return jsonify('Internal server error',500)

    
#class TicketAPI(Resource):
    '''
    def individual_ticket(uuid):
        try:
            ticket = Ticket.query.filter_by(id=uuid).first()
        except:
            return jsonify('Internal server error',500)
        if ticket.creator != current_user.id:
            return jsonify('No access rights, forbidden!',403)
    '''
    
    