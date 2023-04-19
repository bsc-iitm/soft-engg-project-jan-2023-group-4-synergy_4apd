from flask import render_template, request, redirect
from flask_security import login_required, current_user

from backend import app
from backend.database import db
from backend.forms import TicketForm
from backend.models import Ticket, Message

from datetime import datetime


@app.route('/ticket/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm(request.form)

    if request.method == 'POST' and form.validate():

        ticket = Ticket(creator=current_user.id, title=form.title.data, is_public=form.is_public.data)
        db.session.add(ticket)
        db.session.commit()


        message = Message(sender_id=current_user.id, ticket_id=ticket.id, text=form.message.data)
        db.session.add(message)
        db.session.commit()

        return redirect(f'/ticket/{ticket.id}')

    return render_template('dialogs/create_update_dialog.html', form=form,
                           form_title='Create ticket', primary_button_text='Create')


@app.route('/ticket/<id>', methods=['GET'])
@login_required
def view_ticket(id):
    ticket = Ticket.query.filter_by(id=id).first()
    
    messages = Message.query.filter_by(ticket_id=ticket.id).all()

    return render_template('ticket.html', ticket=ticket, messages=messages)


@app.route('/ticket/<id>/reply', methods=['POST'])
@login_required
def add_reply(id):

    ticket = Ticket.query.filter_by(id=id).first()
    
    message = Message(
        sender_id=current_user.id,
        ticket_id=ticket.id,
        text=request.form.get('reply'))
    
    ticket.last_response_time = datetime.utcnow()
    
    db.session.add(message)
    db.session.commit()

    return redirect(f'/ticket/{id}')
