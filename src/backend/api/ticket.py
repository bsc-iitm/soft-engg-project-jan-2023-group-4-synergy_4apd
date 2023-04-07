from flask import request, jsonify
from flask_security import login_required
from models.ticket import Ticket
import uuid

def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        return 'Content-Type not supported!'
    
@app.route('/api/v1/tickets', methods=['GET','POST'])
@login_required
def tickets():
    if request.method == 'POST':
        ticket_data = request.get_json()
        new_ticket = Ticket(
                            id = uuid.uuid4()
                            title = ticket_data['title']
                            status = 
                            votes = 
                            is_public = 
                            creator = 
                            assignee = 
                            solution = 
                            last_response_time = 
                            tags = 
        )
        pass
    elif request.method == 'GET':
        pass
    else:
        return jsonify({'No access rights, forbidden!'},403)