from uuid import uuid4
from backend.models import *

def create_uuid():
    return str(uuid4())

def stringify_tickets(tickets):
    ticket_list = []
    for ticket in tickets:
        ticket_format = {
                            "id": ticket.id,
                            "title": ticket.title,
                            "status": ticket.status,
                            "votes": ticket.votes,
                            "is_public": ticket.is_public,
                            "creator":ticket.creator,
                            "assignee":ticket.assignee,
                            "solution":ticket.solution,
                            "last_response_time": str(ticket.last_response_time),
                            'tags': stringify_tags(ticket.tags)
        }
        ticket_list.append(ticket_format)
    return ticket_list

def stringify_messages(messages):
    message_list = []
    for message in messages:
        message_format = {
                            "id": message.id,
                            "text": message.text,
                            "posted_at": str(message.posted_at),
                            "sender_id": message.sender_id,
                            "ticket_id": message.ticket_id,
                            "hidden": message.hidden,
                            "flagged": message.flagged
        }
        message_list.append(message_format)
    return message_list

def stringify_tags(tags):
    tag_list = []
    for tag in tags:
        tag_format = {
                        "id":tag.id,
                        "name":tag.name,
                        "description":tag.description
        }
        tag_list.append(tag_format)
    return tag_list

def stringify_comments(comments):
    comment_list = []
    for comment in comments:
        comment_format = {
                            "id" : comment.id,
                            "content" : comment.content,
                            "posted_at" : str(comment.posted_at),
                            "article_id" : comment.article_id,
                            "hidden" : comment.hidden
        }
        comment_list.append(comment_format)
    return comment_list

def stringify_articles(articles):
    article_list = []
    for article in articles:
        article_format = {
                            "id": article.id,
                            "creator": article.creator,
                            "title": article.title,
                            "content": article.content,
                            "created_at": str(article.created_at),
                            "updated_at": str(article.updated_at),
                            "tags": stringify_tags(article.tags)
        }
        article_list.append(article_format)
    return article_list

def stringify_notifications(notifications):
    notification_list = []
    for notification in notifications:
        notification_format = {
                            "id" : notification.id,
                            "sender_id" : notification.sender_id,
                            "recipient_id":notification.recipient_id,
                            "content" : notification.content,
                            "action_url" : notification.action_url,
                            "timestamp" : str(notification.timestamp),
                            "read" : notification.read
        }
        notification_list.append(notification_format)
    return notification_list