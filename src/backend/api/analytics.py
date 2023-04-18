from flask_login import current_user
from flask_restful import Resource,reqparse
from backend.models import *
from backend.utils import *

def getTickets():
    tickets=Ticket.query.all()
    return list(tickets)

def getMessages():
    messages=Message.query.all()
    return list(messages)

def getArticles():
    articles=Article.query.all()
    return list(articles)

def getComments():
    comments=Comment.query.all()
    return list(comments)

class AnalyticsAPI(Resource):
            
    def get(self):
        # print(analyticsTickets()
        return 200





  
    