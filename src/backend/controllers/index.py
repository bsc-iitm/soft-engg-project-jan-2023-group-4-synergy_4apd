from flask import render_template, request
from flask_security import login_required, current_user
from backend import app
from backend.models import Ticket

@app.route('/', methods=['GET'])
@login_required
def index():
    tickets = Ticket.query.filter_by(is_public=True).order_by(Ticket.last_response_time.desc()).all()
    return render_template('index.html', tickets=tickets, active_view='public')

@app.route('/my_tickets', methods=['GET'])
@login_required
def my_tickets():
    tickets = Ticket.query.filter_by(creator=current_user.id).order_by(Ticket.last_response_time.desc()).all()
    return render_template('index.html', tickets=tickets, active_view='private')

@app.route('/api_access', methods=['GET'])
@login_required
def api_access():
    return render_template('dialogs/api_access_dialog.html')