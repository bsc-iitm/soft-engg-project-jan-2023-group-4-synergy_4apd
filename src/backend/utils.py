from uuid import uuid4
from backend.models import *
from datetime import datetime

def create_uuid():
    return str(uuid4())

def setTime():
    return datetime.now()

def stringify_tickets(tickets):
    ticket_list = []
    for ticket in tickets:
        ticket_format = {
                            "ticket_id": ticket.id,
                            "Votes": ticket.votes,
                            "title": ticket.title,
                            "status": ticket.status,
                            "last_response_time": str(ticket.last_response_time),
                            'tags': stringify_tags(ticket.tags)
        }
        ticket_list.append(ticket_format)

    return ticket_list

def stringify_messages(messages):
    message_list = []
    for message in messages:
        message_format = {
                            "message_id": message.id,
                            "text": message.text,
                            "sender_id": message.sender_id,
                            "timestamp": str(message.posted_at)
        }
        message_list.append(message_format)

    return message_list

def stringify_tags(tags):
    tag_list = []
    for tag in tags:
        tag_list.append(tag.name)

    return tag_list

def stringify_comments(comments):
    comment_list = []
    for comment in comments:
        comment_format = {
                            "id" : comment.id,
                            "content" : comment.content,
                            "hidden" : comment.hidden
        }
        comment_list.append(comment_format)

    return comment_list

def stringify_articles(articles):
    article_list = []
    for article in articles:
        article_format = {
                            "article_id": article.id,
                            "title": article.title,
                            "content": article.content,
                            "creator": article.creator,
                            "created_at": str(article.created_at),
                            "updated_at": str(article.updated_at),
                            "tags": stringify_tags(article.tags)
        }
        article_list.append(article_format)

    return article_list
