from flask_restful import Resource
from flask_security import roles_required,login_required
from backend.models import *
from backend.utils import *

def getTickets():
    return Ticket.query.all()

def getMessages():
    return Message.query.all()

def getArticles():
    return Article.query.all()

def getComments():
    return Comment.query.all()

def getTags():
    return Tag.query.all()

def getUsers():
    return User.query.all()

def getNotifications():
    return Notification.query.all()

class AnalyticsAPI(Resource):

    @login_required
    @roles_required('admin')        
    def get(self):
        tickets=getTickets()
        openTickets,inProgressTickets,resolvedTickets=0,0,0
        for ticket in tickets:
            if ticket.status==0:
                openTickets+=1
            if ticket.status==1:
                inProgressTickets+=1
            if ticket.status==2:
                resolvedTickets+=1
        totalTickets=len(tickets)

        users=getUsers()
        userStudent,supportStaff,admin,superadmin=0,0,0,0
        for user in users:
            if 'superadmin' in user.roles:
                superadmin+=1
            elif 'admin' in user.roles:
                admin+=1
            elif 'support_staff' in user.roles:
                supportStaff+=1
            else:
                userStudent+=1
        totalUsers=len(users)

        notifications=getNotifications()
        totalNotifications,unreadNotifications,readNotifications=0,0,0
        for notification in notifications:
            if notification.read:
                readNotifications+=1
            else:
                unreadNotifications+=1
        totalNotifications=len(notifications)

        messages=getMessages()
        totalMessages,hiddenMessages,flaggedMessages=0,0,0
        for message in messages:
            if message.flagged:
                flaggedMessages+=1
            if message.hidden:
                hiddenMessages+=1
        totalMessages=len(messages)

        articles=getArticles()
        totalArticles=len(articles)
        
        tags=getTags()
        totalTags=len(tags)

        comments=getComments()
        totalComments,hiddenComments=0,0
        for comment in comments:
            if comment.hidden:
                hiddenComments+=1
        totalComments=len(comments)

        return {
            "message":"Request successful",
            "analytics": {
                "totalTickets":totalTickets,
                "openTickets":openTickets,
                "inProgressTickets":inProgressTickets,
                "resolvedTickets":resolvedTickets,
                "totalUsers":totalUsers,
                "userStudents":userStudent,
                "support_staff":supportStaff,
                "administrators":admin,
                "super_administrators":superadmin,
                "totalNotifications":totalNotifications,
                "unreadNotifications":unreadNotifications,
                "readNotifications":readNotifications,
                "totalMessages":totalMessages,
                "hiddenMessages":hiddenMessages,
                "flaggedMessages":flaggedMessages,
                "totalArticles":totalArticles,
                "totalTags":totalTags,
                "totalComments":totalComments,
                "hiddenComments":hiddenComments
                }
            },200