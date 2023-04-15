from uuid import uuid4
from backend.models import *
from datetime import datetime

def createUUID():
    return str(uuid4())

def setTime():
    return datetime.now()

def stringify_tickets(tickets):
    ticket_list = []
    for ticket in tickets:
        ticket_format = {
                            "ticketID": ticket.id,
                            "Votes": ticket.votes,
                            "title": ticket.title,
                            "Status": ticket.status,
                            "LastResponseTime": str(ticket.last_response_time),
                            'tags': stringify_ticket_tags(ticket.tags)
        }
        ticket_list.append(ticket_format)

    return ticket_list

def stringify_messages(messages):
    message_list = []
    for message in messages:
        message_format = {
                            "messageID": message.id,
                            "text": message.text,
                            "senderID": message.sender_id,
                            "timestamp": str(message.posted_at)
        }
        message_list.append(message_format)

    return message_list

def stringify_ticket_tags(tags):
    tag_list = []
    for tag in tags:
        tag_list.append(tag.name)

    return tag_list