from flask import request, jsonify
from flask_security import login_required
from flask_login import current_user
from models.ticket import Ticket
from models.message import Message
import uuid
    
@app.route('/api/v1/tickets', methods=['GET','POST'])
@login_required
def tickets():
    #POST
    if request.method == 'POST':
        ticket_data = []
        if request.headers.get('Content-Type') == 'application/json':
            ticket_data = request.get_json()
        else:
            return jsonify('Malformed request!',400)
        new_ticket = Ticket(
                            id = uuid.uuid4()
                            title = ticket_data['title']
                            status = 'status'
                            votes = 0
                            is_public = True
                            creator = current_user.id
                            assignee = 'UUID'
                            solution = 'UUID'
                            last_response_time = 'NIL'
                            tags = '1,2,3,'
        )
        try:
            db.session.commit()
            return jsonify('Ticket created successfully',201)
        except:
            return jsonify('Internal server error',500)
        
    #GET
    elif request.method == 'GET':
        try:
            tickets = Ticket.query.filter_by(is_public=True).all()
            return jsonify(tickets, 200)
        except:
            return jsonify('Internal server error',500)
        
    #ERROR
    else:
        return jsonify('No access rights, forbidden!',403)
    
@app.route('/api/v1/mytickets', methods=['GET'])
@login_required
def mytickets():
    #GET
    if request.method == 'GET':
        try:
            tickets = Ticket.query.filter_by(creator=current_user.id).all()
            return jsonify(tickets, 200)
        except:
            return jsonify('Internal server error',500)
        
    #ERROR
    else:
        return jsonify('No access rights, forbidden!',403)
    
@app.route('/api/v1/ticket/<string:uuid>', methods=['GET','PUT','DELETE'])
@login_required
def individual_ticket(uuid):
    try:
        ticket = Ticket.query.filter_by(id=uuid).first()
    except:
        return jsonify('Internal server error',500)
    if ticket.creator != current_user.id:
        return jsonify('No access rights, forbidden!',403)

    #GET
    if request.method == 'GET':
        try:
            messages = Message.query.filter_by(ticket_id=uuid).all()
            return jsonify([
                            'ticketID': ticket.id,
                            'votes': ticket.votes,
                            'title': ticket.title,
                            'status': ticket.status,
                            'solutionID': ticket.solution,
                            'last_response_time': ticket.last_response_time,
                            'messages': messages
            ],200)
        except:
            return jsonify('Internal server error',500)

    #PUT
    elif request.method == 'PUT':        
        ticket_data = []
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
        
    #DELETE
    elif request.method == 'DELETE':
        try:
            db.session.delete(ticket)
            db.session.commit()
            return jsonify('Ticket deleted successfully',200)
        except:
            return jsonify('Internal server error',500)
        
    #ERROR
    else:
        return jsonify('Malformed request!',400)